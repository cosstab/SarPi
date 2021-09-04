from message import SarpiMessage
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


class TelegramAdapter():
	# Initialize adapter, Telegram Updater and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher
        
        # Create the Updater and pass it your bot's token.
        self.updater = Updater('YOUR TOKEN')

        # Get the dispatcher to register handlers
        telegram_dispatcher = self.updater.dispatcher

        # On every received command, on_message function will be executed
        telegram_dispatcher.add_handler(MessageHandler(Filters.command, self._on_command))


    def start(self) -> None:
        # Start the Bot
        self.updater.start_polling()
        
        print('Telegram adapter started. Logged on as ' + self.updater.bot.username + '!')

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


    def _on_command(self, update, context) -> None:
        command, args = self._extract_command_and_args(update.message.text)
        sarpi_message = SarpiMessage(command, args, None)

        # SarPi's dispatcher will send the message to the appropiate module and return the response
        response = self.sarpi_dispatcher.on_command(sarpi_message)

        # Send the response
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
