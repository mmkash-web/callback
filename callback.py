from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/billing/callback1', methods=['POST'])
def callback():
    try:
        # Check if the request is form data
        if request.method == 'POST':
            data = request.form
            logger.info(f"Request form: {data}")

            # Get the M-Pesa message from the request
            mpesa_message = data.get('mpesa_message')
            if not mpesa_message:
                logger.error("M-Pesa message is missing in the request.")
                return jsonify({"error": "M-Pesa message is missing"}), 400

            # Process the message (you can add your logic here)
            logger.info(f"Received M-Pesa message: {mpesa_message}")

            # Example: Respond with success
            return jsonify({"status": "success", "message": "Callback processed"}), 200
        else:
            logger.error("Invalid request method.")
            return jsonify({"error": "Invalid request method"}), 405
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Start the Flask application
    app.run(host='0.0.0.0', port=int(20869))  # Change port as needed
