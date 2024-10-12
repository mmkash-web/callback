from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def is_valid_mpesa_confirmation(mpesa_message: str) -> bool:
    """Validate if the M-Pesa confirmation message is in a valid format."""
    return "Confirmed" in mpesa_message and "Ksh" in mpesa_message

@app.route('/verify', methods=['GET'])
def verify_transaction():
    """Verify if the transaction was successful based on the reference."""
    mpesa_message = request.args.get('mpesa_message')
    
    # Log the received message for debugging
    app.logger.info(f"Received M-Pesa message: {mpesa_message}")
    
    if is_valid_mpesa_confirmation(mpesa_message):
        # Extract information from the message
        try:
            # Parse the M-Pesa message
            transaction_details = parse_mpesa_message(mpesa_message)
            return jsonify({"status": "valid", "message": "Transaction verified successfully.", "details": transaction_details}), 200
        except Exception as e:
            app.logger.error(f"Error parsing M-Pesa message: {str(e)}")
            return jsonify({"status": "invalid", "message": "Error processing the transaction."}), 400
    else:
        app.logger.warning("Invalid M-Pesa confirmation message.")
        return jsonify({"status": "invalid", "message": "Invalid M-Pesa confirmation message."}), 400

def parse_mpesa_message(mpesa_message: str):
    """Parse the M-Pesa confirmation message and extract details."""
    # Split the message by "paid to" to extract details
    try:
        parts = mpesa_message.split("paid to")
        amount_and_details = parts[0].strip()
        payee_and_time = parts[1].strip().split("on")
        
        amount = amount_and_details.split(" ")[1]  # Ksh amount
        payee = payee_and_time[0].strip()  # Payee name
        timestamp = payee_and_time[1].strip()  # Transaction time
        
        return {
            "amount": amount,
            "payee": payee,
            "timestamp": timestamp
        }
    except Exception as e:
        raise ValueError("Failed to parse M-Pesa message") from e

if __name__ == '__main__':
    app.run(debug=True)
