from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.handler import Handler
from telegram.update import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram.bot import BotCommand
from events.chat_member_updated import ChatMemberUpdated
from events.command import SarpiCommand
from user import SarpiUser
from medium import SarpiMedium
import os
from dotenv import load_dotenv


class TelegramAdapter():
    '''
    Telegram adapter will look for native commands (the ones starting with "/") and custom commands (you 
    can select your own prefix for convenience). Disable privacy settings on BotFather for custom commands
    on groups.
    '''

    PLATFORM_NAME = "Telegram"


	# Initialize adapter, Telegram Updater and it's events
    def __init__(self, sarpi_dispatcher: 'SarpiDispatcher') -> None:
        self.sarpi_dispatcher = sarpi_dispatcher
        
        # Load API token and command prefix from environment variables on .env file
        load_dotenv()
        API_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.__ALTERNATIVE_COMMAND_PREFIX = os.getenv('TELEGRAM_COMMAND_PREFIX')

        # Create the Updater and pass it your bot's token.
        self.updater = Updater(API_TOKEN)

        # Get the dispatcher to register handlers
        telegram_dispatcher = self.updater.dispatcher

        # Set on_native_command as the handler of registered native commands
        commands = []

        for command, comand_manager in sarpi_dispatcher.command_managers.items():
            description = comand_manager.description
            commands.append(BotCommand(command, description))
            telegram_dispatcher.add_handler(CommandHandler(command, self._on_native_command))
        
        self.updater.bot.set_my_commands(commands) #Register commands for autocompletion

        # On every message, execute _on_message
        telegram_dispatcher.add_handler(MessageHandler(Filters.text, self._on_message))

        # Handle other events
        telegram_dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, self._on_user_join))

        # Show any other event for testing purposes
        #telegram_dispatcher.add_handler(AnythingHandler(self._on_event))


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
            Native: /alarm@SarPi set 9 am
            Custom: .alarm set 9 am
        """

        text = text[1:] #Remove slash. Now, text = "alarm@SarPi set 9 am"
        text = text.split(' ') #Split text. text = ["alarm@SarPi", "set", "9", "am"]
        command = text[0].split('@')[0] #command = "alarm"
        args = text[1:] #args = ["set", "9", "am"]
        
        return command, args


    def _telegram_to_sarpi_id(self, id: int) -> str:
        return self.PLATFORM_NAME + str(id)


    def _prepare_metadata(self, update: Update, context: CallbackContext):
        # Prepare user metadata
        user = SarpiUser(self._telegram_to_sarpi_id(update.effective_user.id), update.effective_user.username,
                         update.effective_user.first_name)

        # Prepare lambda reply function to be used later by the respective command module.
        # A SarpiMessage object will be provided to this function.
        reply_func = lambda message : context.bot.send_message(chat_id=update.effective_chat.id, text=message.text)

        # Create Medium object with previous data
        medium = SarpiMedium(self.PLATFORM_NAME, self._telegram_to_sarpi_id(update.effective_chat.id), reply_func)

        return medium, user


    def _on_message(self, update: Update, context: CallbackContext) -> None:
        # Check for custom commands
        if update.message.text.startswith(self.__ALTERNATIVE_COMMAND_PREFIX):
            # Prepare command and arguments
            command, args = self._extract_command_and_args(update.message.text)
            self._proccess_command(command, args, update, context)


    def _on_native_command(self, update: Update, context: CallbackContext) -> None:
        # Prepare command and arguments
        command, args = self._extract_command_and_args(update.message.text)
        self._proccess_command(command, args, update, context)


    def _proccess_command(self, command, args, update: Update, context: CallbackContext):
        medium, user = self._prepare_metadata(update, context)

        # Create SarpiCommand object
        sarpi_command = SarpiCommand(update.message.text, command, args, medium, user)

        # SarPi's dispatcher will send the command to the appropiate module
        self.sarpi_dispatcher.on_update(sarpi_command)
    

    def _on_user_join(self, update: Update, context: CallbackContext):
        medium, user = self._prepare_metadata(update, context)

        # We'll create an update for every user who has joined
        for user in update.message.new_chat_members:
            affected_user = SarpiUser(self._telegram_to_sarpi_id(user.id), user.username, user.first_name)
            update = ChatMemberUpdated(ChatMemberUpdated.UpdateType.USER_JOINED, affected_user, 
                                        user.id==self.updater.bot.id, medium, user)
            self.sarpi_dispatcher.on_update(update)


    def _on_event(self, update: Update, context: CallbackContext):
        print("\n\nTelegram Event")
        print(update)


class AnythingHandler(Handler):
    '''
    Testing handler that will trigger the callback function on any not previously handled event
    '''
    def check_update(self, update):
        return True