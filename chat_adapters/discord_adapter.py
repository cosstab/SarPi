import asyncio
from discord.commands.context import ApplicationContext
from discord.member import Member
from discord.commands import Option
from events.chat_member_updated import ChatMemberUpdated
from events.command import SarpiCommand
from medium import SarpiMedium
from user import SarpiUser
import discord
import os
from dotenv import load_dotenv

class DiscordAdapter():
    PLATFORM_NAME = "Discord"

    _waiting_commands = {} #Dict of commands waiting for a response with the chat id as a key

    # Initialize adapter, Discord client and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher

        # Load API token and command prefix from environment variables on .env file
        load_dotenv()
        self.__API_TOKEN = os.getenv('DISCORD_TOKEN')
        COMMAND_PREFIX = os.getenv('DISCORD_COMMAND_PREFIX')

        # Add Discord intents for member updates and message content (needs to be enabled on Discord developer portal)
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
      
        # Create Discord client
        self.bot = discord.Bot(intents=intents)

        # Register slash commands. Command parameters are not available at the moment
        for command, command_manager in sarpi_dispatcher.command_managers.items():
            description = command_manager.description

            slash_command = discord.commands.SlashCommand(func=self._on_slash_command, name=command, description=description)

            if command_manager.has_params:
                for param in command_manager.params: #Add parameters from command managing function
                    opt = Option(param.annotation, name=param.name)
                    opt._parameter_name = param.name
                    slash_command.options.append(opt)

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
            else:
                # Check if we are waiting for a response on this chat from the sender of the message
                try:
                    chat_id = self._get_chat_id(message)
                    w_command = self._waiting_commands[chat_id]

                    if w_command.user.id == self._discord_to_sarpi_id(message.author.id):
                        w_command.args = message.content.split(' ')
                        del self._waiting_commands[chat_id]
                        self.sarpi_dispatcher.on_update(w_command)
                except KeyError:
                    pass
        
        @self.bot.event
        async def on_member_join(member: Member):
            guild = member.guild
            if guild.system_channel is not None:
                # Prepare lambda reply function to be used later by the respective command module.
                # A SarpiMessage object will be provided to this function.
                loop = asyncio.get_event_loop()
                reply_func = lambda response : loop.create_task(guild.system_channel.send(response.text[:2000]))

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
        try:
            if user.nick is None:
                display_name = user.name
            else:
                display_name = user.nick
        except AttributeError:
            display_name = user.name
        
        return SarpiUser(self._discord_to_sarpi_id(user.id), user.name, display_name)
    

    def _get_chat_id(self, message) -> str:
        # Check if author of the message is a member of a server or an user via DM
        if isinstance(message.author, discord.Member):
            return self._discord_to_sarpi_id(message.author.guild)
        else: #Author is chatting via DM
            return self._discord_to_sarpi_id(message.author.id)


    async def _on_custom_command(self, message) -> None:
        # Prepare lambda reply function to be used later by the respective command module.
        # A SarpiMessage object will be provided to this function.
        loop = asyncio.get_event_loop()
        reply_func = lambda response : loop.create_task(message.channel.send(response.text[:2000]))

        await self._on_command(message, reply_func)


    async def _on_slash_command(self, ctx: ApplicationContext, **kwargs) -> None:
        # Prepare lambda reply function to be used later by the respective command module.
        # A SarpiMessage object will be provided to this function.
        loop = asyncio.get_event_loop()
        reply_func = lambda response : loop.create_task(ctx.respond(response.text[:2000]))

        command = ctx.command.name
        ctx.content = "/" + command #Adapt context to message, since message object is not available.
        
        # Add slash command arguments to message content
        for argument in kwargs.values():
            ctx.content += " " + str(argument)
        
        await self._on_command(ctx, reply_func, **kwargs)


    async def _on_command(self, message, reply_func, **kwargs):
        # Prepare command and arguments
        command, args = self._extract_command_and_args(message.content)

        # Prepare user metadata        
        user = self._discord_to_sarpi_user(message.author)

        chat_id = self._get_chat_id(message)

        # Create Medium object with previous data
        medium = SarpiMedium(self.PLATFORM_NAME, chat_id, reply_func)

        # Create SarpiCommand object
        sarpi_command = SarpiCommand(message.content, command, args, medium, user)

        # SarPi's dispatcher will send the command to the appropiate module
        if self.sarpi_dispatcher.on_update(sarpi_command, **kwargs):
            # When True is returned, we add the command to the list of commands waiting for a response
            self._waiting_commands[chat_id] = sarpi_command
        