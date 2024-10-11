from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load existing mappings from JSON files
def load_user_mapping():
    try:
        with open('user_mapping.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_http_links():
    try:
        with open('http_links.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Send message via Telegram bot
def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/sendMessage"
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

    # Load user mapping and HTTP links
    user_mapping = load_user_mapping()
    http_links = load_http_links()

    if status:
        # Associate the transaction ID with the user ID and HTTP Injector link
        chat_id = user_mapping.get(user_id)
        if chat_id:
            # Store the transaction ID and corresponding HTTP link
            http_links[transaction_id] = "<HTTP_INJECTOR_LINK>"  # Replace with actual link
            user_mapping[transaction_id] = chat_id
            with open('user_mapping.json', 'w') as f:
                json.dump(user_mapping, f)
            with open('http_links.json', 'w') as f:
                json.dump(http_links, f)
            message = f"Payment Successful!\nTransaction ID: {transaction_id}\nPlease verify your transaction by sending this ID."
            send_message(chat_id, message)
        else:
            app.logger.warning("No chat ID found for user ID: %s", user_id)
    else:
        app.logger.warning("Payment not successful for Transaction ID: %s", transaction_id)

    return jsonify({"status": "success"}), 200

# Command to verify transaction ID
@app.route('/verify', methods=['POST'])
def verify_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')
    chat_id = data.get('chat_id')

    app.logger.info("Verification request received for Transaction ID: %s", transaction_id)

    # Load HTTP links
    http_links = load_http_links()

    # Check if transaction ID is valid
    if transaction_id in http_links:
        injector_link = http_links[transaction_id]
        send_message(chat_id, f"Your HTTP Injector Link: {injector_link}")
    else:
        send_message(chat_id, "Invalid Transaction ID. Please try again.")

    return jsonify({"status": "verified"}), 200

if __name__ == '__main__':
    app.run(debug=True)
