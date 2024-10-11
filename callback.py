from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample transaction status storage
transactions = {}

# Route for receiving the STK push callback
@app.route('/billing/callback1', methods=['POST'])
def handle_callback():
    # Get the data sent by M-Pesa (or PayHero)
    data = request.json
    transaction_id = data.get("transaction_id")
    payment_status = data.get("status")
    payment_phone_number = data.get("phone_number")

    # Update the transaction status
    if transaction_id in transactions:
        transactions[transaction_id]["status"] = payment_status
        transactions[transaction_id]["phone_number"] = payment_phone_number

    return jsonify({"result": "Success"}), 200


# Route for initiating the STK push (this would be called by the bot)
@app.route('/initiate_stk_push', methods=['POST'])
def initiate_stk_push():
    # This is where you initiate the STK push request using the PayHero API or Daraja
    request_data = request.json

    # Simulate initiating STK push and store in transactions
    transaction_id = request_data.get("transaction_id")
    user_phone_number = request_data.get("phone_number")

    # Store the transaction details
    transactions[transaction_id] = {"status": "pending", "phone_number": user_phone_number}

    # Respond to the bot with the transaction details
    return jsonify({"transaction_id": transaction_id, "status": "pending"}), 200


# Route for checking payment status (this would be called by the bot)
@app.route('/check_payment_status/<transaction_id>', methods=['GET'])
def check_payment_status(transaction_id):
    # Retrieve the transaction details
    if transaction_id in transactions:
        status = transactions[transaction_id]["status"]
        phone_number = transactions[transaction_id]["phone_number"]
        return jsonify({"status": status, "phone_number": phone_number})
    else:
        return jsonify({"error": "Transaction not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
