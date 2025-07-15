# News Summary and WhatsApp Notification

This project fetches the latest news headlines using the NewsAPI and sends a summary to a specified WhatsApp number using Twilio's API.

## Setup Instructions

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following variables:
   ```
   NEWS_API_KEY=your_newsapi_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_SENDER_NUMBER=your_twilio_sender_number
   RECIPIENT_NUMBER=recipient_whatsapp_number
   ```
4. Run the script:
   ```
   python news.py
   ```

## Project Structure

```
/News
  ├── news.py                # Main script
  ├── .env                   # Environment variables
  ├── requirements.txt       # Dependencies
  ├── README.md              # Project documentation
```

## Features
- Fetches top news headlines.
- Sends a WhatsApp message with the news summary.