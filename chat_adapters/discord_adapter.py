from message import SarpiMessage
import discord
from discord.ext import commands

class DiscordAdapter():
    __COMMAND_PREFIX = '.' #Select your favorite command prefix

    # Initialize adapter, Discord client and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher
        
        # Create Discord client
        self.bot = discord.Client()

        @self.bot.event
        async def on_ready():
            print('Discord adapter started. Logged on as {0}!'.format(self.bot.user))

        # This event will run on every received message
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if message.content.startswith(self.__COMMAND_PREFIX):
                await self._on_command(message)

    
    async def start(self) -> None:
        await self.bot.start('YOUR TOKEN')

    
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


    async def _on_command(self, message) -> None:
        command, args = self._extract_command_and_args(message.content)

        sarpi_message = SarpiMessage(command, args, None)

        # SarPi's dispatcher will send the message to the appropiate module and return the response
        response = self.sarpi_dispatcher.on_command(sarpi_message)

        # Send the response
        await message.channel.send(response)
