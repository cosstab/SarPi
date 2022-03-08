import asyncio
from discord.commands.context import ApplicationContext
from discord.member import Member
from events.chat_member_updated import ChatMemberUpdated
from events.command import SarpiCommand
from medium import SarpiMedium
from user import SarpiUser
import discord
import os
from dotenv import load_dotenv

class DiscordAdapter():
    PLATFORM_NAME = "Discord"

    # Initialize adapter, Discord client and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher

        # Load API token and command prefix from environment variables on .env file
        load_dotenv()
        self.__API_TOKEN = os.getenv('DISCORD_TOKEN')
        COMMAND_PREFIX = os.getenv('DISCORD_COMMAND_PREFIX')

        # Add Discord intents for member updates
        intents = discord.Intents.default()
        intents.members = True
      
        # Create Discord client
        self.bot = discord.Bot(intents=intents)

        # Register slash commands. Command parameters are not available at the moment
        for command in sarpi_dispatcher.command_managers:
            slash_command = discord.commands.SlashCommand(func=self._on_slash_command, name=command)
            self.bot.add_application_command(slash_command)

        @self.bot.event
        async def on_ready():
            print(self.PLATFORM_NAME + ' adapter started. Logged on as {0}!'.format(self.bot.user))

        # This event will run on every received message
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if message.content.startswith(COMMAND_PREFIX):
                await self._on_custom_command(message)
        
        @self.bot.event
        async def on_member_join(member: Member):
            guild = member.guild
            if guild.system_channel is not None:
                # Prepare lambda reply function to be used later by the respective command module.
                # A SarpiMessage object will be provided to this function.
                loop = asyncio.get_event_loop()
                reply_func = lambda response : loop.create_task(guild.system_channel.send(response.text))

                user = self._discord_to_sarpi_user(member)
                medium = SarpiMedium(self.PLATFORM_NAME, self._discord_to_sarpi_id(member.guild), reply_func)
                update = ChatMemberUpdated(ChatMemberUpdated.UpdateType.USER_JOINED, user, False, medium, user)

                self.sarpi_dispatcher.on_update(update)

    
    async def start(self) -> None:
        # Start bot
        await self.bot.start(self.__API_TOKEN)

    
    def _extract_command_and_args(self, text: str) -> str:
        """
        Command example:
            .alarm set 9 am
        """

        text = text[1:] #Remove dot. Now, text = "alarm set 9 am"
        text = text.split(' ') #Split text. text = ["alarm", "set", "9", "am"]
        command = text[0] #command = "alarm"
        args = text[1:] #args = ["set", "9", "am"]
        
        return command, args


    def _discord_to_sarpi_id(self, id: int) -> str:
        return self.PLATFORM_NAME + str(id)
    

    def _discord_to_sarpi_user(self, user: discord.User) -> SarpiUser:
        # Check if user has a nickname
        if user.nick is None:
            display_name = user.name
        else:
            display_name = user.nick
        
        return SarpiUser(self._discord_to_sarpi_id(user.id), user.name, display_name)


    async def _on_custom_command(self, message) -> None:
        # Prepare command and arguments
        command, args = self._extract_command_and_args(message.content)

        # Prepare lambda reply function to be used later by the respective command module.
        # A SarpiMessage object will be provided to this function.
        loop = asyncio.get_event_loop()
        reply_func = lambda response : loop.create_task(message.channel.send(response.text))

        await self._on_command(message, reply_func, command, args)


    async def _on_slash_command(self, ctx: ApplicationContext) -> None:
        # Prepare lambda reply function to be used later by the respective command module.
        # A SarpiMessage object will be provided to this function.
        loop = asyncio.get_event_loop()
        reply_func = lambda response : loop.create_task(ctx.respond(response.text))

        command = ctx.command.name
        ctx.content = "/" + command #Adapt context to message, since message object is not available.
        
        await self._on_command(ctx, reply_func, command)


    async def _on_command(self, message, reply_func, command, args=[]):
        # Prepare user metadata        
        user = self._discord_to_sarpi_user(message.author)

        # Check if author of the message is a member of a server or an user via DM
        if isinstance(message.author, discord.Member):
            chat_id = self._discord_to_sarpi_id(message.author.guild)
        else: #Author is chatting via DM
            chat_id = self._discord_to_sarpi_id(message.author.id)

        # Create Medium object with previous data
        medium = SarpiMedium(self.PLATFORM_NAME, chat_id, reply_func)

        # Create SarpiCommand object
        sarpi_command = SarpiCommand(message.content, command, args, medium, user)

        # SarPi's dispatcher will send the command to the appropiate module
        self.sarpi_dispatcher.on_update(sarpi_command)
        