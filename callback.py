from flask import Flask, request, jsonify
import logging
from telegram import Bot

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/billing/callback1', methods=['POST'])  # Ensure this matches your callback URL
def payment_callback():
    try:
        # Get JSON data from M-Pesa callback
        data = request.get_json()
        logging.info(f"Received callback data: {data}")

        # Validate the incoming data structure
        if 'response' not in data or 'Status' not in data['response']:
            logging.error("Invalid callback data format")
            return jsonify({"status": "error", "message": "Invalid format"}), 400

        amount = data['response'].get('Amount', 0)
        transaction_reference = data['response'].get('Transaction_Reference')
        payment_status = data['response'].get('Payment_Method')  # Change as needed based on your needs

        # Process payment confirmation
        if payment_status == "MPESA":
            notify_user(transaction_reference, payment_status)
        else:
            logging.warning(f"Payment not completed for transaction reference: {transaction_reference}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

def notify_user(transaction_reference, status):
    user_id = get_user_id_from_transaction(transaction_reference)
    logging.info(f"Attempting to notify user with ID: {user_id} for transaction: {transaction_reference}")

    if user_id:
        try:
            bot.send_message(chat_id=user_id, text=f"Payment successful for transaction reference: {transaction_reference}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
    else:
        logging.error(f"No user ID found for transaction reference: {transaction_reference}")

def get_user_id_from_transaction(transaction_reference):
    # Replace this with your logic to find the user ID based on transaction_reference
    # This can be a database lookup or a mapping stored in memory
    user_id_mapping = {
        'INV-009': 12345678,  # Example mapping
        # Add more mappings as needed
    }
    return user_id_mapping.get(transaction_reference)

if __name__ == '__main__':
    app.run(debug=True)
