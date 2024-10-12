from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Simulated transaction data for demonstration purposes
transaction_data = {
    "INV-009": {"status": "confirmed"},
    # Add more transactions as needed
}

@app.route('/')
def home():
    return "Welcome to the M-Pesa Callback Handler!"

@app.route('/billing/callback1', methods=['POST'])
def handle_billing_callback():
    """Handle incoming M-Pesa confirmation messages for billing."""
    data = request.json
    app.logger.info(f"Received data: {data}")  # Log the incoming data

    transaction_reference = data.get("transaction_reference")
    mpesa_confirmation_message = data.get("mpesa_confirmation_message")

    if transaction_reference and mpesa_confirmation_message:
        # Verify transaction reference and status
        transaction_info = transaction_data.get(transaction_reference)

        if transaction_info and transaction_info["status"] == "confirmed":
            return jsonify({"status": "confirmed"}), 200
        else:
            return jsonify({"status": "unverified"}), 400
    else:
        return jsonify({"error": "Missing parameters"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=57576)
