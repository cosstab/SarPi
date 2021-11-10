import asyncio
from medium import SarpiMedium
from user import SarpiUser
from message import SarpiMessage
import discord
import os
from dotenv import load_dotenv

class DiscordAdapter():
    PLATFORM_NAME = "Discord"
    __COMMAND_PREFIX = '.' #Select your favorite command prefix

    # Initialize adapter, Discord client and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher
        
        # Create Discord client
        self.bot = discord.Client()

        @self.bot.event
        async def on_ready():
            print(self.PLATFORM_NAME + ' adapter started. Logged on as {0}!'.format(self.bot.user))

        # This event will run on every received message
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if message.content.startswith(self.__COMMAND_PREFIX):
                await self._on_command(message)

    
    async def start(self) -> None:
        # Load API token from environment variables on .env file
        load_dotenv()
        API_TOKEN = os.getenv('DISCORD_TOKEN')

        # Start bot
        await self.bot.start(API_TOKEN)

    
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

    async def _on_command(self, message) -> None:
        # Prepare command and arguments
        command, args = self._extract_command_and_args(message.content)

        # Check if author of the message is a member of a server or an user via DM
        if isinstance(message.author, discord.Member):
            display_name = message.author.nick
            chat_id = message.author.guild
        elif isinstance(message.author, discord.User):
            display_name = None
            chat_id = self._discord_to_sarpi_id(message.author.id)

        # Prepare user metadata        
        user = SarpiUser(self._discord_to_sarpi_id(message.author.id), message.author.name, display_name)

        # Prepare lambda reply function to be used later by the respective command module.
        # A Message object will be provided to this function.
        loop = asyncio.get_event_loop()
        reply_func = lambda response : loop.create_task(message.channel.send(response.text))

        # Create Medium object with previous data
        medium = SarpiMedium(self.PLATFORM_NAME, chat_id, reply_func)

        # Create Message object
        sarpi_message = SarpiMessage(message.content, command, args, medium, user)

        # SarPi's dispatcher will send the message to the appropiate module
        self.sarpi_dispatcher.on_command(sarpi_message)
