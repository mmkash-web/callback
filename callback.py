from flask import Flask, request, jsonify
import logging
import os
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the transaction logs to keep track of confirmations
transaction_log = {}

@app.route('/verify_transaction', methods=['POST'])
def verify_transaction():
    """Verify the M-Pesa transaction using the provided reference and confirmation message."""
    data = request.json
    transaction_reference = data.get('transaction_reference')
    mpesa_confirmation_message = data.get('mpesa_confirmation_message')

    if not transaction_reference or not mpesa_confirmation_message:
        return jsonify({"error": "Invalid data provided"}), 400

    # Verify the transaction reference and confirmation message
    if transaction_reference in transaction_log:
        return jsonify({"verified": False, "message": "Transaction has already been confirmed."}), 200

    if is_valid_mpesa_confirmation(mpesa_confirmation_message):
        # Log the transaction as confirmed
        transaction_log[transaction_reference] = {
            "confirmed": True,
            "confirmation_message": mpesa_confirmation_message
        }
        return jsonify({"verified": True}), 200
    else:
        return jsonify({"verified": False, "message": "Invalid M-Pesa confirmation message format."}), 200

def is_valid_mpesa_confirmation(message: str) -> bool:
    """Check if the M-Pesa confirmation message is in a valid format."""
    # Implement your logic here to check the confirmation message format
    return "Payment" in message and "of" in message

if __name__ == '__main__':
    app.run(debug=True)

