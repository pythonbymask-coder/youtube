import os
import time
import uuid
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Token
TELEGRAM_TOKEN = ""

# Folder on your PC where Google Drive syncs files
GOOGLE_DRIVE_FOLDER = r"E:\My Drive\txt2img"

# API endpoint
API_URL = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a message and I’ll process it.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.chat_id

    # Step 1: Acknowledge receipt
    await update.message.reply_text("✅ Your message received. Processing...")

    # Step 2: Generate UUID for the file
    file_uuid = str(uuid.uuid4())
    expected_filename = f"{file_uuid}.png"   # extension can be .pdf, .docx etc.
    filepath = os.path.join(GOOGLE_DRIVE_FOLDER, expected_filename)

    # Step 3: Call your API with message + uuid
    try:
        response = requests.post(API_URL, json={
            "prompt": user_message,
            "img_name": file_uuid
        })
        response.raise_for_status()
    except Exception as e:
        await update.message.reply_text(f"❌ API call failed: {e}")
        return

    # Step 4: Wait until file with uuid appears in Google Drive folder
    await update.message.reply_text(f"⏳ Waiting for txt2img ...")
    print(f"Image name: {file_uuid}")

    timeout = 300  # max 5 minutes wait
    waited = 0
    while not os.path.exists(filepath) and waited < timeout:
        time.sleep(5)
        waited += 5


    # Step 5: Send file back to user as IMAGE
    if os.path.exists(filepath):
        with open(filepath, "rb") as img:
            await context.bot.send_photo(chat_id=user_id, photo=img)
    else:
        await update.message.reply_text("❌ File was not created within timeout.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
