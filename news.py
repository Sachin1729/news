from newsapi import NewsApiClient
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, jsonify
import os
import schedule
import time
import signal
import threading

# Load environment variables from the .env file
load_dotenv()

# Initialize News API client
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

# Initialize Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

app = Flask(__name__)

# Function to fetch and send news
def send_news():
    # Fetch top headlines
    top = newsapi.get_top_headlines(language="en", page_size=10)

    # Collect the news headlines and format them into a message body
    news_summary = "\n".join([f"- {article['title']} ({article['url']})" for article in top["articles"][:5]])

    # Get recipient and sender numbers from environment variables
    recipient_number = os.getenv("RECIPIENT_NUMBER")
    sender_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

    # Send the message via Twilio
    message = client.messages.create(
        from_='whatsapp:' + sender_number,
        body=f'Hello Sachin! Your AI news summary is ready 🧠📬\n\n{news_summary}',
        to='whatsapp:' + recipient_number
    )

    print("Message SID:", message.sid)

# Load schedule time from environment variables
schedule_time = os.getenv("SCHEDULE_TIME", "07:30")  # Default to 07:30 if not set

# Schedule the news to be sent daily at the specified time
schedule.every().day.at(schedule_time).do(send_news)

# Graceful shutdown handler
def graceful_shutdown(signum, frame):
    print("\nScheduler stopped gracefully.")
    exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, graceful_shutdown)

# Flask route to trigger news summary manually
@app.route("/send-news", methods=["POST"])
def trigger_send_news():
    try:
        send_news()
        return jsonify({"message": "News summary sent successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to check the health of the application
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

port = int(os.getenv("PORT", 5000))  # Load port from environment variables, default to 5000 if not set

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=port)

