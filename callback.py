from flask import Flask, request, jsonify
import logging
import json

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

    # Extract details from the callback
    transaction_id = data.get('transaction_id')  # Example key, adjust as per your payload
    user_id = data.get('user_id')  # Example key, adjust as per your payload
    amount = data.get('amount')  # Example key, adjust as per your payload

    # Store the transaction (you may want to adjust this based on your data structure)
    transactions[transaction_id] = {
        "user_id": user_id,
        "amount": amount,
        "status": "confirmed",
        "timestamp": data.get('timestamp')  # Example key, adjust as per your payload
    }

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
    else:
        response_message = {"error": "Invalid Transaction ID"}

    return jsonify(response_message), 200

if __name__ == '__main__':
    app.run(debug=True)
