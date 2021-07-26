from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


class TelegramAdapter():
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher

    def start(self) -> None:
        # Create the Updater and pass it your bot's token.
        updater = Updater("YOUR TOKEN")

        # Get the dispatcher to register handlers
        telegram_dispatcher = updater.dispatcher

        # On every received command, on_message function will be executed
        telegram_dispatcher.add_handler(MessageHandler(Filters.command, self.on_message))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def __extract_command_and_args(self, text: str) -> str:
        """
        Command example:
            /alarm@SarPi set 9 am
        """

        text = text[1:] #Remove slash. Now, text = "alarm@SarPi set 9 am"
        text = text.split(" ") #Split text. text = ["alarm@SarPi", "set", "9", "am"]
        command = text[0].split("@")[0] #command = "alarm"
        args = text[1:] #args = ["set", "9", "am"]
        
        return command, args

    def on_message(self, update, context) -> None:
        command, args = self.__extract_command_and_args(update.message.text)

        # SarPi's dispatcher will send the command to the appropiate module and return the response
        response = self.sarpi_dispatcher.on_message(command, args)

        # Send the response
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
