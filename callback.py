from flask import Flask, request, jsonify
import logging
import os
from telegram import Bot
import asyncio

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the Telegram Bot with the token from an environment variable
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')  # Use environment variable
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for Flask application")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/billing/callback1', methods=['POST'])  # Ensure this matches your callback URL
def payment_callback():
    try:
        # Get JSON data from PayHero
        data = request.get_json()
        logging.info(f"Received callback data: {data}")

        # Validate the incoming data structure
        if 'response' not in data or 'Amount' not in data['response'] or 'Transaction_Reference' not in data['response']:
            logging.error("Invalid callback data format")
            return jsonify({"status": "error", "message": "Invalid format"}), 400

        amount = data['response']['Amount']
        transaction_reference = data['response']['Transaction_Reference']
        payment_status = data['response'].get('woocommerce_payment_status', 'unknown')  # Adjust as needed

        # Process payment confirmation
        if payment_status == "complete":
            asyncio.run(notify_user(transaction_reference, payment_status))
        else:
            logging.warning(f"Payment not completed for transaction reference: {transaction_reference}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

async def notify_user(transaction_reference, status):
    # Your logic to notify the user on Telegram about the successful payment
    user_id = get_user_id_from_transaction(transaction_reference)  # Implement this function
    if user_id:
        try:
            await bot.send_message(chat_id=user_id, text=f"Payment successful for transaction reference: {transaction_reference}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

def get_user_id_from_transaction(transaction_reference):
    # Implement logic to retrieve user_id associated with the transaction_reference
    return 12345678  # Replace with actual user ID retrieval logic

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable provided by Heroku
    app.run(host='0.0.0.0', port=port)  # Bind to all interfaces

