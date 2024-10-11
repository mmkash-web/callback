
from flask import Flask, request, jsonify
import logging
import os
from telegram import Bot

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
        if 'transaction_id' not in data or 'status' not in data:
            logging.error("Invalid callback data format")
            return jsonify({"status": "error", "message": "Invalid format"}), 400

        transaction_id = data['transaction_id']
        status = data['status']

        # Process payment confirmation
        if status == "success":
            notify_user(transaction_id, status)
        else:
            logging.warning(f"Payment failed for transaction ID: {transaction_id}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

def notify_user(transaction_id, status):
    # Your logic to notify the user on Telegram about the successful payment
    user_id = get_user_id_from_transaction(transaction_id)  # Implement this function
    if user_id:
        try:
            bot.send_message(chat_id=user_id, text=f"Payment successful for transaction ID: {transaction_id}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

def get_user_id_from_transaction(transaction_id):
    # Implement logic to retrieve user_id associated with the transaction_id
    return 12345678  # Replace with actual user ID retrieval logic

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable provided by Heroku
    app.run(host='0.0.0.0', port=port)  # Bind to all IPs
