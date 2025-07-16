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
   SCHEDULE_TIME=HH:MM  # Time to send the news daily (24-hour format, default is 07:30)
   PORT=8000  # Port number for the Flask application
   ```
4. Run the script:
   ```
   python news.py
   ```

## API Keys and Configuration

To use this project, you need to obtain the following API keys and credentials:

1. **NewsAPI Key**:
   - Visit [NewsAPI](https://newsapi.org/) and sign up for a free account.
   - Generate an API key from your account dashboard.

2. **Twilio Credentials**:
   - Visit [Twilio](https://www.twilio.com/) and sign up for a free account.
   - Obtain your `Account SID` and `Auth Token` from the Twilio Console.
   - Set up a Twilio WhatsApp sender number by following Twilio's [WhatsApp setup guide](https://www.twilio.com/whatsapp).

Update the `.env` file with these credentials as shown in the setup instructions above.

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

## Graceful Shutdown

The script now includes a feature to handle interruptions gracefully. If you press `Ctrl+C` while the script is running, it will stop the scheduler and exit cleanly with a message.