from flask import Flask, request, jsonify
import logging
import re

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual user ID and message storage
user_id = "USER_ID_PLACEHOLDER"
user_messages = {}

@app.route('/billing/callback1', methods=['POST'])
def billing_callback():
    # Log the entire request for debugging
    app.logger.info(f"Request data: {request.data}")
    app.logger.info(f"Request form: {request.form}")
    app.logger.info(f"Request headers: {request.headers}")

    mpesa_message = request.form.get('mpesa_message')

    if not mpesa_message:
        app.logger.error("M-Pesa message is missing in the request.")
        return jsonify({"error": "M-Pesa message is missing."}), 400

    # Process the incoming message
    try:
        app.logger.info(f"Received M-Pesa message: {mpesa_message}")

        # Store the message for the user
        if user_id not in user_messages:
            user_messages[user_id] = []
        user_messages[user_id].append(mpesa_message)

        # Example parsing logic: extract the amount paid
        amount_paid = re.search(r'Ksh([\d,]+\.?\d*)', mpesa_message)
        if amount_paid:
            amount_paid = amount_paid.group(1).replace(",", "")
            app.logger.info(f"Amount paid: Ksh{amount_paid}")
        else:
            app.logger.warning("Failed to extract amount from the M-Pesa message.")

    except Exception as e:
        app.logger.error(f"Error processing M-Pesa message: {e}")
        return jsonify({"error": "Failed to process M-Pesa message."}), 500

    return jsonify({"status": "success"}), 200


@app.route('/verify', methods=['GET'])
def verify_message():
    mpesa_message = request.args.get('mpesa_message')

    if not mpesa_message:
        app.logger.error("M-Pesa message is missing in the request.")
        return jsonify({"error": "M-Pesa message is missing."}), 400

    # Example verification logic
    # Here you would implement your logic to compare the message with user input
    app.logger.info(f"Verifying M-Pesa message: {mpesa_message}")
    # Simulate verification logic
    if mpesa_message in user_messages.get(user_id, []):
        return jsonify({"status": "verified", "message": "Message matches."}), 200
    else:
        return jsonify({"status": "not_verified", "message": "Message does not match."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20869)
