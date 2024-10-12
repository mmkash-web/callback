from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

app = Flask(__name__)

# Replace these with your actual username and password
username = quote_plus("admin@admin")  # URL-encode your username
password = quote_plus("9kosc8pHZGqeS74nmt0B")  # URL-encode your password

# MongoDB connection string (replace <username> and <password>)
MONGODB_URI = f"mongodb://{username}:{password}@node1-f8ca9d4f542f00de.database.cloud.ovh.net,node2-f8ca9d4f542f00de.database.cloud.ovh.net,node3-f8ca9d4f542f00de.database.cloud.ovh.net/admin?replicaSet=replicaset&tls=true"
client = MongoClient(MONGODB_URI)
db = client['your_database_name']  # Replace with your actual database name

@app.route('/billing/callback1', methods=['POST'])
def callback():
    # Get the JSON data from the request
    data = request.json
    
    # Log the received data
    app.logger.info(f'Received data: {data}')
    
    # Example of processing the data
    if not data or 'mpesa_message' not in data:
        return jsonify({'error': 'M-Pesa message is missing'}), 400

    mpesa_message = data['mpesa_message']
    
    # Save the message to the MongoDB collection
    db.messages.insert_one({'message': mpesa_message})
    
    return jsonify({'message': 'Callback received successfully'}), 200

@app.route('/verify', methods=['GET'])
def verify():
    mpesa_message = request.args.get('mpesa_message')
    
    # Log the received M-Pesa message
    app.logger.info(f'Verifying M-Pesa message: {mpesa_message}')
    
    if not mpesa_message:
        return jsonify({'error': 'M-Pesa message is missing in the request.'}), 400

    return jsonify({'status': 'Message verified successfully', 'message': mpesa_message}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
