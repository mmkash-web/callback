from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your Flask app URL for verification
FLASK_APP_URL = "https://callback1-21e1c9a49f0d.herokuapp.com"

@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa callback."""
    data = request.get_json()
    app.logger.info("Received M-Pesa Callback: %s", data)
    
    # Validate the callback data
    if not validate_mpesa_data(data):
        app.logger.error("Invalid callback data: %s", data)
        return jsonify({"error": "Invalid callback data"}), 400

    # Extract necessary fields
    transaction_id = data['response']['Transaction_Reference']
    mpesa_confirmation_message = data  # Store the entire message for verification

    # Verify the transaction
    if verify_transaction_with_flask(transaction_id, mpesa_confirmation_message):
        app.logger.info("Transaction %s verified successfully.", transaction_id)
        return jsonify({"status": "success"}), 200
    else:
        app.logger.error("Transaction verification failed for %s.", transaction_id)
        return jsonify({"status": "verification failed"}), 400

def validate_mpesa_data(data):
    """Validate incoming M-Pesa callback data."""
    # Implement your validation logic here
    if 'response' in data and 'Transaction_Reference' in data['response']:
        return True
    return False

def verify_transaction_with_flask(transaction_id: str, mpesa_confirmation_message: dict) -> bool:
    """Verify the transaction with the Flask app."""
    url = f"{FLASK_APP_URL}/verify"
    payload = {
        "transaction_id": transaction_id,
        "confirmation_message": mpesa_confirmation_message
    }
    response = requests.post(url, json=payload)
    
    # Check if the verification was successful
    if response.status_code == 200:
        return True
    return False

@app.route('/verify', methods=['POST'])
def verify_transaction():
    """Verify the transaction."""
    data = request.get_json()
    app.logger.info("Verifying transaction: %s", data)
    
    # Implement your verification logic here
    transaction_id = data.get("transaction_id")
    if transaction_id:
        # Here you would normally verify the transaction with your database or M-Pesa API
        return jsonify({"status": "verified", "transaction_id": transaction_id}), 200
    
    return jsonify({"error": "Transaction ID missing"}), 400

if __name__ == '__main__':
    app.run(debug=True)
