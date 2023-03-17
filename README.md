# LINE Chatbot Translator

This LINE chatbot application translates the content of a URL into the selected language using Google Translate and returns the translated text as a PDF file. The chatbot is built using Python, Flask, LINE Messaging API SDK, and Googletrans.

## Features

- Detects user-sent URLs
- Presents a Quick Reply with language options
- Translates the content of the URL using Google Translate
- Generates a PDF with the translated text
- Sends the PDF to the user

## Requirements

- Python 3.7 or later
- Flask
- LINE Messaging API SDK for Python
- Requests
- Googletrans
- FPDF

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/line-chatbot-translator.git
cd line-chatbot-translator
```

2. Install the required Python packages: pip install -r requirements.txt
3. Set the environment variables:

- `LINE_CHANNEL_SECRET`: Your LINE channel secret
- `LINE_CHANNEL_ACCESS_TOKEN`: Your LINE channel access token
- `BASE_URL`: The base URL of your application, e.g., `https://your-app.vercel.app`

## Usage

1. Run the application locally: python app.py
2. Deploy the application to Vercel (optional):

- Install Vercel CLI: `npm install -g vercel`
- Deploy the application: `vercel`

3. Set the webhook URL for your LINE Messaging API Channel to `https://your-app.vercel.app/callback`.
4. Start chatting with your LINE chatbot by sending a URL. The chatbot will provide a list of language options to choose from. Once a language is selected, the chatbot will translate the text at the URL, generate a PDF file containing the translated text, and send it to the user.
