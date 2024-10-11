import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Constants
FLASK_API_BASE_URL = "https://callback1-21e1c9a49f0d.herokuapp.com"  # Update with your actual Flask API URL
API_TOKEN = "7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ"  # Replace with your actual Telegram Bot API token

# Setup basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Bingwa Sokoni data and SMS deals!")

async def enter_mpesa_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transaction_id = context.user_data.get("transaction_id")
    user_phone_number = context.user_data.get("user_phone_number")

    # Check the payment status
    payment_status, payment_phone_number = await check_payment_status(transaction_id)
    if payment_status == "successful":
        if payment_phone_number == user_phone_number:
            await update.message.reply_text("Payment successful! Your order is confirmed.")
        else:
            await update.message.reply_text("Payment confirmed, but phone number does not match.")
    else:
        await update.message.reply_text("Payment not successful yet. Please wait.")

async def check_payment_status(transaction_id):
    response = requests.get(f"{FLASK_API_BASE_URL}/check_payment_status/{transaction_id}")
    if response.status_code == 200:
        data = response.json()
        return data["status"], data["phone_number"]
    else:
        logging.error(f"Failed to check payment status for transaction ID {transaction_id}. Response: {response.text}")
        return None, None

async def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enter_mpesa_confirmation))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
