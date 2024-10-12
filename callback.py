from flask import Flask, request, jsonify
import re
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    logging.info(f"Received data: {data}")

    # Assuming 'Body' contains the confirmation message
    confirmation_message = data.get('Body', {}).get('Callback', {}).get('Message', '')
    
    # Parse the confirmation message
    parsed_message = parse_mpesa_confirmation_message(confirmation_message)

    if parsed_message:
        transaction_id = parsed_message['transaction_id']
        logging.info(f"Transaction ID {transaction_id} verified successfully.")
        # Here, you can implement further logic to handle the transaction
        return jsonify({'status': 'verified', 'transaction_id': transaction_id}), 200
    else:
        logging.error("Invalid M-Pesa confirmation message format.")
        return jsonify({'status': 'error', 'message': 'Invalid M-Pesa confirmation message format.'}), 400

def parse_mpesa_confirmation_message(message):
    # Regular expression to extract fields from the message
    pattern = (r'(?P<transaction_id>\w+) Confirmed\. Ksh(?P<amount>[\d,]+\.\d{2}) paid to '
               r'(?P<recipient>.+?) on (?P<date>\d{2}/\d{2}/\d{2}) at (?P<time>\d{1,2}:\d{2} [APM]{2})\. '
               r'New M-PESA balance is Ksh(?P<new_balance>[\d,]+\.\d{2})\. '
               r'Transaction cost, Ksh(?P<transaction_cost>[\d,]+\.\d{2})\. '
               r'Amount you can transact within the day is (?P<daily_limit>[\d,]+\.\d{2})\. '
               r'Download new M-PESA app on (?P<promotion_link>http[^\s]+)\s& get \d+MB FREE data\.')

    match = re.match(pattern, message)
    if match:
        return match.groupdict()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
