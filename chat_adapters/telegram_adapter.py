from user import SarpiUser
from medium import SarpiMedium
from message import SarpiMessage
from telegram.ext import Updater, MessageHandler, Filters
import os
from dotenv import load_dotenv


class TelegramAdapter():
    PLATFORM_NAME = "Telegram"

	# Initialize adapter, Telegram Updater and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher
        
        # Load API token from environment variables on .env file
        load_dotenv()
        API_TOKEN = os.getenv('TELEGRAM_TOKEN')

        # Create the Updater and pass it your bot's token.
        self.updater = Updater(API_TOKEN)

        # Get the dispatcher to register handlers
        telegram_dispatcher = self.updater.dispatcher

        # On every received command, on_message function will be executed
        telegram_dispatcher.add_handler(MessageHandler(Filters.command, self._on_command))


    def start(self) -> None:
        # Start the Bot
        self.updater.start_polling()
        
        print(self.PLATFORM_NAME + ' adapter started. Logged on as ' + self.updater.bot.username + '!')

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        #updater.idle()


    def _extract_command_and_args(self, text: str) -> str:
        """
        Command example:
            /alarm@SarPi set 9 am
        """

        text = text[1:] #Remove slash. Now, text = "alarm@SarPi set 9 am"
        text = text.split(' ') #Split text. text = ["alarm@SarPi", "set", "9", "am"]
        command = text[0].split('@')[0] #command = "alarm"
        args = text[1:] #args = ["set", "9", "am"]
        
        return command, args

    def _telegram_to_sarpi_id(self, id: int) -> str:
        return self.PLATFORM_NAME + str(id)

    def _on_command(self, update, context) -> None:
        # Prepare command and arguments
        command, args = self._extract_command_and_args(update.message.text)

        # Prepare user metadata
        user = SarpiUser(self._telegram_to_sarpi_id(update.effective_user.id), update.effective_user.username, update.effective_user.first_name)

        # Prepare lambda reply function to be used later by the respective command module.
        # A Message object will be provided to this function.
        reply_func = lambda message : context.bot.send_message(chat_id=update.effective_chat.id, text=message.text)

        # Create Medium object with previous data
        medium = SarpiMedium(self.PLATFORM_NAME, self._telegram_to_sarpi_id(update.effective_chat.id), reply_func)

        # Create Message object
        sarpi_message = SarpiMessage(update.message.text, command, args, medium, user)

        # SarPi's dispatcher will send the message to the appropiate module
        self.sarpi_dispatcher.on_command(sarpi_message)
