from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your actual Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ'
CHAT_ID = '1870796520'

def send_telegram_message(message):
    """Send a message to the Telegram bot."""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    return response.json()

@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    # Log the incoming data for debugging
    data = request.json
    print("Received data:", data)  # Log the received data

    # Check if 'response' key exists
    if 'response' not in data:
        return jsonify({"error": "Invalid M-Pesa confirmation message format. 'response' key missing."}), 400

    # Extracting relevant fields from the response
    response_data = data['response']
    
    # Define required fields
    required_fields = ['Transaction_Reference', 'Amount', 'Source', 'Transaction_Date']

    for field in required_fields:
        if field not in response_data:
            print(f"Missing field: {field}")
            return jsonify({"error": f"Invalid M-Pesa confirmation message format. Missing field: {field}."}), 400

    # Log successful validation
    print("All required fields are present.")

    # Send a message to Telegram about the successful payment
    send_telegram_message(f"Payment received:\n"
                          f"Transaction Reference: {response_data['Transaction_Reference']}\n"
                          f"Amount: Ksh {response_data['Amount']}\n"
                          f"Source: {response_data['Source']}\n"
                          f"Transaction Date: {response_data['Transaction_Date']}")

    # Process the data here (e.g., save the transaction details to your database)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
