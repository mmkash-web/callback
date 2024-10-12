from flask import Flask, request, jsonify

app = Flask(__name__)

transaction_store = {}

@app.route('/callback', methods=['POST'])
def mpesa_callback():
    """Receive callback from PayHero and store transaction status."""
    data = request.json
    transaction_reference = data.get('transaction_reference')
    status = data.get('status')

    # Store the transaction details in a temporary store
    transaction_store[transaction_reference] = status
    
    return jsonify({"message": "Callback received"}), 200

@app.route('/verify', methods=['GET'])
def verify_transaction():
    """Verify if the transaction was successful based on the reference."""
    transaction_reference = request.args.get('transaction_reference')
    status = transaction_store.get(transaction_reference, "Failed")

    return jsonify({"transaction_reference": transaction_reference, "status": status})

if __name__ == '__main__':
    app.run(debug=True)
