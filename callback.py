from flask import Flask, request, jsonify
import logging
import re

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Sample in-memory storage for transactions (replace with your database in production)
transactions = {}

# Callback endpoint for M-Pesa
@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    data = request.json
    app.logger.info("Received M-Pesa Callback: %s", data)

    # Extract details from the callback message (replace with actual payload keys if needed)
    message = data.get('message', '')  # assuming 'message' contains the transaction details
    transaction_id = extract_transaction_id(message)
    user_id = data.get('user_id')  # Adjust according to actual payload structure
    amount = data.get('amount')  # Adjust according to actual payload structure
    timestamp = data.get('timestamp')  # Adjust according to actual payload structure

    if not transaction_id or not user_id or not amount:
        app.logger.error("Invalid callback data: %s", data)
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    # Store the transaction
    transactions[transaction_id] = {
        "user_id": user_id,
        "amount": amount,
        "status": "confirmed",
        "timestamp": timestamp
    }

    app.logger.info("Transaction stored: %s", transactions[transaction_id])
    return jsonify({"status": "success"}), 200

# Verification endpoint
@app.route('/verify_transaction', methods=['POST'])
def verify_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')

    app.logger.info("Verification request received for Transaction ID: %s", transaction_id)

    # Check if transaction ID is valid
    if transaction_id in transactions:
        transaction_details = transactions[transaction_id]
        response_message = {
            "transaction_id": transaction_id,
            "user_id": transaction_details["user_id"],
            "status": transaction_details["status"],
            "amount": transaction_details["amount"],
            "timestamp": transaction_details["timestamp"]
        }
        app.logger.info("Transaction verified: %s", response_message)
    else:
        response_message = {"error": "Invalid Transaction ID"}
        app.logger.warning("Transaction ID not found: %s", transaction_id)

    return jsonify(response_message), 200

# Helper function to extract transaction ID from message
def extract_transaction_id(message):
    # Use regex to extract the transaction ID (assuming it follows a similar pattern to SJC7RUCLTD)
    match = re.search(r'\b[A-Z0-9]{10}\b', message)  # Modify the regex if needed
    return match.group(0) if match else None

if __name__ == '__main__':
    app.run(debug=True)
