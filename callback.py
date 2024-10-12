import re
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/verify', methods=['GET'])
def verify_mpesa_message():
    # Extract the M-Pesa message from the query parameters
    mpesa_message = request.args.get('mpesa_message', '')

    if not mpesa_message:
        logger.error("No M-Pesa message provided")
        return jsonify({'error': 'No M-Pesa message provided'}), 400

    logger.info(f"Received M-Pesa message: {mpesa_message}")

    # Regex to extract the relevant information from the M-Pesa message
    pattern = r"(?P<code>SJC[0-9]+) Confirmed\. Ksh(?P<amount>[0-9.]+) paid to (?P<recipient>.+?) on (?P<date>[0-9/]+) at (?P<time>[0-9: ]+)\. New M-PESA balance is Ksh(?P<balance>[0-9.]+)\. Transaction cost, Ksh(?P<cost>[0-9.]+)\."
    match = re.match(pattern, mpesa_message)

    if match:
        details = match.groupdict()
        logger.info(f"Parsed M-Pesa message details: {details}")
        # You can process the details further as needed
        return jsonify(details), 200
    else:
        logger.error("Error parsing M-Pesa message: Failed to parse M-Pesa message")
        return jsonify({'error': 'Failed to parse M-Pesa message'}), 400

if __name__ == '__main__':
    app.run(debug=True)
