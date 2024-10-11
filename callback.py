from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ'
CHAT_ID = 'YOUR_CHAT_ID'  # Optional, for initial testing or admin notifications

# Create or load the user chat IDs and transaction mapping
def load_mapping():
    if os.path.exists('user_mapping.json'):
        with open('user_mapping.json', 'r') as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    with open('user_mapping.json', 'w') as f:
        json.dump(mapping, f)

# Store user transaction details when they initiate a purchase
def store_user_transaction(chat_id, transaction_id):
    mapping = load_mapping()
    mapping[transaction_id] = chat_id
    save_mapping(mapping)

# Send a notification to Telegram
def send_notification_to_telegram(chat_id, transaction_id, phone_number):
    message = f"Payment Successful!\nTransaction ID: {transaction_id}\nPhone Number: {phone_number}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    return response.json()

# Endpoint for handling incoming payments
@app.route('/billing/callback1', methods=['POST'])
def callback():
    data = request.json
    app.logger.info("Incoming JSON data: %s", data)

    # Extract payment details from the JSON data
    transaction_id = data.get('response', {}).get('Transaction_Reference')
    phone_number = data.get('response', {}).get('Source')
    status = data.get('status')

    app.logger.info("Payment Callback Received: Transaction ID: %s, Status: %s, Phone Number: %s", transaction_id, status, phone_number)

    # Load mapping to get user chat ID
    mapping = load_mapping()
    chat_id = mapping.get(transaction_id)

    if status:
        if chat_id:
            send_notification_to_telegram(chat_id, transaction_id, phone_number)
        else:
            app.logger.warning("No chat ID found for Transaction ID: %s", transaction_id)
        return "Payment processed successfully", 200
    else:
        app.logger.warning("Payment not successful for Transaction ID: %s", transaction_id)
        return "Payment processing failed", 400

# Example function to initiate a purchase and store user transaction
def initiate_purchase(chat_id, transaction_id):
    # Your existing purchase logic here...
    
    # Store user transaction details
    store_user_transaction(chat_id, transaction_id)

    # Continue with the purchase process...
    # For example, send the user a message confirming the purchase initiation
    message = "Your purchase has been initiated."
    send_notification_to_telegram(chat_id, "Transaction initiated", message)

if __name__ == "__main__":
    app.run(port=5000)
