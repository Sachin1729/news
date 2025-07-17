import json
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
twilio_template_sid = os.getenv("TWILIO_TEMPLATE_SID")
client = Client(account_sid, auth_token)

app = Flask(__name__)

# Function to fetch and send news
def send_news():
    # Fetch top headlines
    top = newsapi.get_top_headlines(language="en", page_size=5)  # Limit to 5 articles for scheduled news

    # Collect the news headlines and format them into a message body
    news_summary = "\n".join([f"- {article['title']} ({article['url']})" for article in top["articles"]])

    # Get recipient and sender numbers from environment variables
    recipient_number = os.getenv("RECIPIENT_NUMBER")
    sender_number = os.getenv("TWILIO_SENDER_NUMBER")

    # Validate sender and recipient numbers
    if not sender_number or not recipient_number:
        raise ValueError("TWILIO_SENDER_NUMBER and RECIPIENT_NUMBER must be set in the environment variables.")

    # Send the message via Twilio
    message = client.messages.create(
        from_='whatsapp:' + sender_number,
        to='whatsapp:' + recipient_number,
        content_sid={twilio_template_sid},  # Use SID OR use content_template with variables
        content_variables=json.dumps({
            "1": "Sachin",
            "2": "🧠📬\n\n"+str(news_summary),
            "3": "\n\nThis is an automated message from NewsAI."
        }),
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
        send_news()  # Call the send_news function to send the news
        
        # Fetch top headlines
        top = newsapi.get_top_headlines(language="en", page_size=10)

        # Collect the news headlines and format them into a response body
        news_summary = "\n".join([f"- {article['title']} ({article['url']})" for article in top["articles"]])

        return jsonify({"message": "News summary fetched successfully.", "news": news_summary}), 200
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

