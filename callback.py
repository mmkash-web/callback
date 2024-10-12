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
    transaction_id = data['response'].get('Transaction_Reference')
    if transaction_id is None:
        app.logger.error("Transaction Reference is missing: %s", data)
        return jsonify({"error": "Transaction Reference missing"}), 400

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
    if 'response' in data:
        if 'Transaction_Reference' in data['response']:
            return True
        else:
            app.logger.error("Missing Transaction_Reference in response: %s", data)
    else:
        app.logger.error("Missing response in callback data: %s", data)
    return False

def verify_transaction_with_flask(transaction_id: str, mpesa_confirmation_message: dict) -> bool:
    """Verify the transaction with the Flask app."""
    url = f"{FLASK_APP_URL}/verify"
    payload = {
        "transaction_id": transaction_id,
        "confirmation_message": mpesa_confirmation_message
    }
    
    app.logger.info("Sending verification request to Flask app: %s", payload)
    
    try:
        response = requests.post(url, json=payload)
        app.logger.info("Verification response from Flask app: %s", response.json())
        
        # Check if the verification was successful
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException as e:
        app.logger.error("Error during verification request: %s", e)
    
    return False

@app.route('/verify', methods=['POST'])
def verify_transaction():
    """Verify the transaction."""
    data = request.get_json()
    app.logger.info("Verifying transaction data received: %s", data)

    transaction_id = data.get("transaction_id")
    if transaction_id:
        # Here you would normally verify the transaction with your database or M-Pesa API
        app.logger.info("Transaction ID %s verified successfully.", transaction_id)
        return jsonify({"status": "verified", "transaction_id": transaction_id}), 200

    app.logger.error("Transaction ID missing in received data: %s", data)
    return jsonify({"error": "Transaction ID missing"}), 400

if __name__ == '__main__':
    app.run(debug=True)
