from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for demonstration purposes
# In a real application, you might want to use a database to store transaction references and their statuses
transaction_data = {
    "INV-009": {"amount": 80, "status": "confirmed"},  # Example transaction
    # Add other transactions here if needed
}

@app.route('/callback', methods=['POST'])
def handle_callback():
    """Handle incoming M-Pesa confirmation messages."""
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
    app.run(debug=True, port=5000)  # Change port if needed
