from flask import Flask, request, jsonify
import logging
import re

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dummy in-memory storage for user requests (replace with a database in production)
user_requests = {}

@app.route('/billing/callback1', methods=['POST'])
def billing_callback():
    try:
        # Log the entire request form for debugging
        app.logger.info(f"Request form: {request.form}")

        # Get the mpesa_message from the request
        mpesa_message = request.form.get('mpesa_message')
        
        if mpesa_message is None:
            app.logger.error("M-Pesa message is missing in the request.")
            return jsonify({"status": "error", "message": "M-Pesa message is missing."}), 400
        
        # Log the received message
        app.logger.info(f"Received M-Pesa message: {mpesa_message}")

        # Example regex to extract necessary information (customize as needed)
        pattern = r"(?P<transaction_id>SJC\d+)\s+Confirmed\.\s+Ksh(?P<amount>\d+(\.\d+)?)\s+paid\s+to\s+(?P<recipient>.+?)\s+on\s+(?P<date>\d{1,2}/\d{1,2}/\d{2,4})\s+at\s+(?P<time>\d{1,2}:\d{2}\s+[AP]M)\."
        match = re.search(pattern, mpesa_message)

        if match:
            transaction_id = match.group('transaction_id')
            amount = match.group('amount')
            recipient = match.group('recipient')
            date = match.group('date')
            time = match.group('time')

            # Log the parsed information
            app.logger.info(f"Transaction ID: {transaction_id}, Amount: Ksh{amount}, Recipient: {recipient}, Date: {date}, Time: {time}")

            # Compare with user requests
            if transaction_id in user_requests:
                user_amount = user_requests[transaction_id]  # Assume this holds the amount user requested
                if user_amount == amount:
                    app.logger.info("Transaction amount matches user's request.")
                    # Process the transaction further, e.g., mark it as successful
                else:
                    app.logger.warning("Transaction amount does not match user's request.")
            else:
                app.logger.warning("Transaction ID not found in user requests.")

            return jsonify({"status": "success", "message": "Callback processed successfully."}), 200
        else:
            app.logger.error("Error parsing M-Pesa message: Failed to parse M-Pesa message")
            return jsonify({"status": "error", "message": "Failed to parse M-Pesa message"}), 400

    except Exception as e:
        app.logger.error(f"Error processing callback: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/request_payment', methods=['POST'])
def request_payment():
    # Dummy endpoint for user payment requests
    transaction_id = request.form.get('transaction_id')
    amount = request.form.get('amount')

    # Store the user request (replace with a database in production)
    user_requests[transaction_id] = amount
    return jsonify({"status": "success", "message": "Payment request stored."}), 200

if __name__ == '__main__':
    app.run(debug=True)
