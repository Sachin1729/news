from newsapi import NewsApiClient
from twilio.rest import Client
from dotenv import load_dotenv
import os
import schedule
import time
import signal

# Load environment variables from the .env file
load_dotenv()

# Initialize News API client
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

# Initialize Twilio client
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

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

# Schedule the news to be sent daily at 11:30 AM
schedule.every().day.at("07:30").do(send_news)

# Graceful shutdown handler
def graceful_shutdown(signum, frame):
    print("\nScheduler stopped gracefully.")
    exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, graceful_shutdown)

# Run the scheduler
if __name__ == "__main__":
    print("Scheduler is running. Waiting to send daily news...")
    while True:
        schedule.run_pending()
        time.sleep(60)
