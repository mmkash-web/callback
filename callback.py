from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = '7626726530:AAHnNs51Ew8_lZEnD0VLXkAJBvpAVyRzLig'
# Your Telegram chat ID (you can get this by sending a message to your bot and checking the updates)
CHAT_ID = '1870796520'

# Route to handle M-Pesa callback
@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    # Log the incoming data for debugging
    data = request.json
    print("Received data:", data)  # Log the received data

    # Validate the structure of the data
    if not validate_mpesa_data(data):
        return jsonify({"error": "Invalid M-Pesa confirmation message format."}), 400

    # Send a message to Telegram about the successful payment
    send_telegram_message("Payment received: " + str(data))

    # Process the data here (e.g., save the transaction details to your database)

    return jsonify({"status": "success"}), 200

def validate_mpesa_data(data):
    # Implement your validation logic here
    required_fields = ['transactionId', 'amount', 'phoneNumber', 'transactionTime']

    for field in required_fields:
        if field not in data:
            print(f"Missing field: {field}")
            return False

    return True

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Failed to send message to Telegram:", response.text)

if __name__ == "__main__":
    app.run(debug=True)
