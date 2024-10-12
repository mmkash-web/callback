import re
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Updated regex pattern for M-Pesa confirmation message
def parse_mpesa_confirmation_message(message):
    pattern = (r'(?P<transaction_id>\w+) Confirmed\. Ksh(?P<amount>[\d,]+\.\d{2}) paid to '
               r'(?P<recipient>.+?)\. on (?P<date>\d{2}/\d{2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]{2})\. '
               r'New M-PESA balance is Ksh(?P<new_balance>[\d,]+\.\d{2})\. '
               r'Transaction cost, Ksh(?P<transaction_cost>[\d,]+\.\d{2})\. '
               r'Amount you can transact within the day is (?P<daily_limit>[\d,]+\.\d{2})\. '
               r'Download new M-PESA app on (?P<promotion_link>http[^\s]+) & get \d+MB FREE data\.')
    
    match = re.match(pattern, message)
    if match:
        return match.groupdict()
    else:
        return None

@app.route('/verify', methods=['POST'])
def verify_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')

    # Validate the transaction ID
    if not transaction_id:
        return jsonify({"status": "error", "message": "Transaction ID is required."}), 400

    logging.info(f"Verifying transaction ID: {transaction_id}")

    # Log the confirmation message received (this should be the actual message received)
    confirmation_message = data.get('confirmation_message')  # Assume confirmation message comes in the request
    if confirmation_message:
        logging.info(f"Received confirmation message: {confirmation_message}")
    else:
        return jsonify({"status": "error", "message": "Confirmation message is required."}), 400

    # Parse the confirmation message
    parsed_data = parse_mpesa_confirmation_message(confirmation_message)
    
    if parsed_data and parsed_data['transaction_id'] == transaction_id:
        logging.info(f"Transaction ID {transaction_id} verified successfully.")
        return jsonify({"status": "verified", "transaction_id": transaction_id}), 200
    else:
        logging.error(f"Invalid M-Pesa confirmation message format for Transaction ID: {transaction_id}.")
        return jsonify({"status": "error", "message": "Invalid M-Pesa confirmation message format. Please try again."}), 400

if __name__ == '__main__':
    app.run(debug=True)
