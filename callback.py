from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory transaction data (replace this with your actual data source)
transaction_data = {
    "INV-009": {"status": "confirmed"},
    # Add other transaction references as needed
}

@app.route('/billing/callback', methods=['POST'])
def handle_callback():
    """Handle incoming M-Pesa confirmation messages."""
    data = request.json
    transaction_reference = data.get("transaction_reference")
    mpesa_confirmation_message = data.get("mpesa_confirmation_message")

    if transaction_reference and mpesa_confirmation_message:
        # Process the callback message as needed
        return jsonify({"message": "Callback received", "data": data}), 200
    else:
        return jsonify({"error": "Missing parameters"}), 400

@app.route('/billing/callback1', methods=['POST'])
def handle_billing_callback():
    """Handle incoming M-Pesa confirmation messages for billing."""
    data = request.json
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
