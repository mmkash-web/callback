from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load existing mappings from JSON files
def load_transactions():
    try:
        with open('transactions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_transaction(transaction_id, transaction_data):
    transactions = load_transactions()
    transactions[transaction_id] = transaction_data
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f)

# Send message via Telegram bot
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot<7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ>/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    return response.json()

# Payment callback route
@app.route('/billing/callback1', methods=['POST'])
def callback():
    data = request.json
    transaction_id = data.get('response', {}).get('Transaction_Reference')
    status = data.get('status')
    user_id = data.get('response', {}).get('Source')  # Get user's phone number or identifier

    app.logger.info("Payment Callback Received: Transaction ID: %s, Status: %s", transaction_id, status)

    if status:  # Only store successful transactions
        transaction_data = {
            "user_id": user_id,
            "status": status,
            "amount": data.get('response', {}).get('Amount'),
            "timestamp": data.get('response', {}).get('Transaction_Date')
        }
        save_transaction(transaction_id, transaction_data)  # Save transaction
        message = f"Payment Successful!\nTransaction ID: {transaction_id}\nPlease verify your transaction by sending this ID."
        
        # Optionally send a message to the user (assuming you have a way to get chat_id)
        # chat_id = user_mapping.get(user_id)  # Implement user mapping if needed
        # send_message(chat_id, message)

    else:
        app.logger.warning("Payment not successful for Transaction ID: %s", transaction_id)

    return jsonify({"status": "success"}), 200

# Command to verify transaction ID
@app.route('/verify', methods=['POST'])
def verify_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')

    app.logger.info("Verification request received for Transaction ID: %s", transaction_id)

    # Load transactions
    transactions = load_transactions()

    # Check if transaction ID is valid
    if transaction_id in transactions:
        transaction_details = transactions[transaction_id]
        response_message = (f"Transaction ID: {transaction_id}\n"
                            f"User ID: {transaction_details['user_id']}\n"
                            f"Status: {transaction_details['status']}\n"
                            f"Amount: {transaction_details['amount']}\n"
                            f"Timestamp: {transaction_details['timestamp']}")
    else:
        response_message = "Invalid Transaction ID. Please try again."

    return jsonify({"status": "verified", "message": response_message}), 200

if __name__ == '__main__':
    app.run(debug=True)
