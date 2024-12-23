from telegram import Update
from telegram.ext import Application, CommandHandler,filters,CallbackContext,MessageHandler
import logging
import webbrowser
import os
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
BOT_TOKEN = "7769049127:AAE2yaSy31fMbLmrpJXzJRsuXIvShqBHbOM"

# Initialize the application
application = Application.builder().token(BOT_TOKEN).build()

# Define the start command handler
async def start(update: Update, context):
    await update.message.reply_text("Hello! How can I help you?")
# Define the unknown command handler
async def unknown_command(update: Update, context):
    await update.message.reply_text("Sorry, I didn't understand that command. Please use a valid command.")
#openning yt
async def open_yt(update:Update,context):
    webbrowser.open("https://www.youtube.com/")
    await update.message.reply_text("opeing yotube")
#open fav video
async def play_vid(upadate:Update,context):
      webbrowser.open("https://www.youtube.com/watch?v=HvBccTXuQ0w")
      await upadate.message.reply_text("playing video")
# Command to put the laptop to sleep
async def sleep_laptop(update: Update, context):
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
        await update.message.reply_text("sleeping the pc")
        # Command to shut down the laptop
async def shutdown_laptop(update: Update, context):
        os.system("shutdown /s /t 0")
        await update.message.reply_text("sleeping the pc")
        #close the edge
async def close(update: Update, context):
          os.system("taskkill /IM msedge.exe /F")
          await update.message.reply_text("Closing Microsoft Edge...")
# Add the start command handler to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("yto",open_yt))
application.add_handler(CommandHandler("sleep",sleep_laptop))
application.add_handler(CommandHandler("shutdown",shutdown_laptop))
application.add_handler(CommandHandler("close",close))
#application.add_handler(CommandHandler("openwhat",open_what))
application.add_handler(CommandHandler("play",play_vid))
application.add_handler(MessageHandler(filters.COMMAND,unknown_command))
# Start the bot
if __name__ == "__main__":
    print("Bot started...")
    application.run_polling()
