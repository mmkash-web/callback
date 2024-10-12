import os
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://admin%40admin:9kosc8pHZGqeS74nmt0B@mongodb-542f00de-o22372ca4.database.cloud.ovh.net/admin?replicaSet=replicaset&tls=true')
client = MongoClient(MONGODB_URI)
db = client['your_database_name']  # Replace with your actual database name
mpesa_collection = db['mpesa_messages']  # Collection to store M-Pesa messages

# Your Telegram bot token
TELEGRAM_BOT_TOKEN = '7480076460:AAGieUKKaivtNGoMDSVKeMBuMOICJ9IKJgQ'  # Replace with your actual token
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/billing/callback1', methods=['POST'])
def mpesa_callback():
    # Get data from M-Pesa callback
    data = request.json
    # Ensure the message exists
    if not data or 'message' not in data:
        return jsonify({"error": "M-Pesa message is missing"}), 400
    
    # Insert the M-Pesa message into the database
    mpesa_collection.insert_one(data)
    return jsonify({"success": "Message stored"}), 200

@app.route('/retrieve', methods=['GET'])
def retrieve_messages():
    # Retrieve all M-Pesa messages from the database
    messages = list(mpesa_collection.find())
    # Convert MongoDB documents to a serializable format
    for message in messages:
        message['_id'] = str(message['_id'])  # Convert ObjectId to string
    return jsonify(messages), 200

# Function to handle commands
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to Bingwa Sokoni data and SMS deals!')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

def main():
    # Set up the Telegram bot handlers
    from telegram.ext import Updater
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    
    # Register handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Run Flask app
    app.run(port=os.environ.get('PORT', 5000))
