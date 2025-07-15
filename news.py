from newsapi import NewsApiClient
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Replace hardcoded API keys with environment variables
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

top = newsapi.get_top_headlines(language="en", page_size=10)
for article in top["articles"]:
    print("-", article["title"], article["url"])

# Collect the news headlines and format them into a message body
# Limit the number of news articles to 5 to avoid exceeding the message body limit
news_summary = "\n".join([f"- {article['title']} ({article['url']})" for article in top["articles"][:5]])

# Update the recipient number to use an environment variable
recipient_number = os.getenv("RECIPIENT_NUMBER")
sender_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Update the message body to include the limited news summary
message = client.messages.create(
  from_='whatsapp:'+sender_number,     # Twilio sandbox number
  body=f'Hello Sachin! Your AI news summary is ready 🧠📬\n\n{news_summary}',
  to=f'whatsapp:{recipient_number}'  # Use the recipient number from the environment variable
)

print("Message SID:", message.sid)