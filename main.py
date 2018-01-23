import bot
import utils


settings = utils.get_settings()
bot = bot.Bot(settings["bot_settings"])
bot.run()
