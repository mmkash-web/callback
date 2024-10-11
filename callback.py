from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Store transactions in memory for this example
transactions = {}

# Setup basic logging
logging.basicConfig(level=logging.INFO)

@app.route('/billing/callback1', methods=['POST'])
def handle_callback():
    data = request.json
    transaction_id = data.get("transaction_id")
    payment_status = data.get("status")
    payment_phone_number = data.get("phone_number")

    # Log incoming data for debugging
    logging.info(f"Received callback data: {data}")

    # Update the transaction status
    if transaction_id in transactions:
        transactions[transaction_id]["status"] = payment_status
        transactions[transaction_id]["phone_number"] = payment_phone_number
        logging.info(f"Updated transaction: {transactions[transaction_id]}")
    else:
        logging.warning(f"Transaction ID {transaction_id} not found.")

    return jsonify({"result": "Success"}), 200

@app.route('/check_payment_status/<transaction_id>', methods=['GET'])
def check_payment_status(transaction_id):
    if transaction_id in transactions:
        return jsonify(transactions[transaction_id]), 200
    else:
        return jsonify({"error": "Transaction not found"}), 404

# Dummy endpoint to simulate transaction creation (for testing purposes)
@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    transaction_id = data.get("transaction_id")
    transactions[transaction_id] = {
        "status": "pending",
        "phone_number": data.get("phone_number"),
    }
    return jsonify({"result": "Transaction created", "transaction_id": transaction_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
