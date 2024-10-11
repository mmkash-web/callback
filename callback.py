from flask import Flask, request, jsonify
import logging
from telegram import Bot

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/billing/callback1', methods=['POST'])
def payment_callback():
    try:
        # Get JSON data from M-Pesa callback
        data = request.get_json()
        logging.info(f"Received callback data: {data}")

        # Validate the incoming data structure
        if 'response' not in data:
            logging.error("Invalid callback data format")
            return jsonify({"status": "error", "message": "Invalid format"}), 400

        response = data['response']
        transaction_reference = response.get('MPESA_Reference') or response.get('Transaction_Reference')
        amount = response.get('Amount', 0)
        payment_method = response.get('Payment_Method', 'Unknown')
        payment_status = response.get('Status') or response.get('woocommerce_payment_status')

        # Ensure required fields are present
        if not transaction_reference or not payment_status:
            logging.error("Transaction reference or status missing")
            return jsonify({"status": "error", "message": "Missing transaction reference or status"}), 400

        # Process payment confirmation
        if payment_status.lower() in ["success", "complete"]:
            notify_user(transaction_reference, payment_status, amount)
            logging.info(f"Payment processed for transaction reference: {transaction_reference}, amount: {amount}")
        else:
            logging.warning(f"Payment not completed for transaction reference: {transaction_reference}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logging.error(f"Error processing callback: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

def notify_user(transaction_reference, status, amount):
    user_id = get_user_id_from_transaction(transaction_reference)
    logging.info(f"Attempting to notify user with ID: {user_id} for transaction: {transaction_reference}")

    if user_id:
        try:
            # Send a more detailed message to Telegram
            message = f"Payment successful for transaction reference: {transaction_reference}\nAmount: {amount} KES\nStatus: {status}"
            bot.send_message(chat_id=user_id, text=message)
            logging.info(f"Message sent to user ID {user_id}: {message}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
    else:
        logging.error(f"No user ID found for transaction reference: {transaction_reference}")

def get_user_id_from_transaction(transaction_reference):
    # Replace this with your logic to find the user ID based on transaction_reference
    user_id_mapping = {
        'INV-009': 12345678,  # Example mapping
        # Add more mappings as needed
    }
    return user_id_mapping.get(transaction_reference)

if __name__ == '__main__':
    app.run(debug=True)
