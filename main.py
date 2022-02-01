from threading import Thread
import asyncio
from dispatcher import SarpiDispatcher

# Import chat adapters
from chat_adapters.telegram_adapter import TelegramAdapter
from chat_adapters.discord_adapter import DiscordAdapter


# Instantiate the dispatcher, which will select the right module to parse the received command
sarpi_dispatcher = SarpiDispatcher()

# Instantiate chat adapters and indicate the dispatcher
telegram = TelegramAdapter(sarpi_dispatcher)
discord = DiscordAdapter(sarpi_dispatcher)

# Start chat adapters on new threads
# Telegram
telegram_thread = Thread(target = telegram.start, args = ())
telegram_thread.start()

# Discord
asyncio.get_child_watcher()
loop = asyncio.get_event_loop()
loop.create_task(discord.start())
discord_thread = Thread(target=loop.run_forever)
discord_thread.start()

# Wait until every adapter finished it's execution
telegram_thread.join()
discord_thread.join()
