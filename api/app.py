import os
import tempfile
import requests
from googletrans import LANGUAGES, Translator
from fpdf import FPDF
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FileMessage, QuickReply, QuickReplyButton, PostbackAction, PostbackEvent
from flask import Flask, request, abort, send_from_directory

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
translator = Translator()

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text

    if is_url(user_text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Please choose the target language:",
                quick_reply=QuickReply(items=language_quick_reply_buttons())
            )
        )
        return

def is_url(text):
    return "http://" in text or "https://" in text

def language_quick_reply_buttons():
    top_languages = [("zh-TW", "Traditional Chinese"), ("en", "English"), ("es", "Spanish"), ("de", "German"), ("fr", "French"), ("it", "Italian"),
                     ("pt", "Portuguese"), ("ru", "Russian"), ("zh-CN", "Chinese"), ("ja", "Japanese"), ("ko", "Korean")]

    buttons = []
    for code, name in top_languages:
        action = PostbackAction(label=name, data=f"translate_{code}")
        button = QuickReplyButton(action=action)
        buttons.append(button)

    return buttons

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data.startswith("translate_"):
        user_language = data.split("_")[1]
        translated_text = translate_text(user_language)
        create_and_send_pdf(translated_text, event.source.user_id)
        return

def translate_text(language):
    # Fetch the URL content
    response = requests.get(url)
    text = response.text

    # Translate the text
    translated = translator.translate(text, dest=language)
    return translated.text

def create_and_send_pdf(translated_text, user_id):
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, translated_text)
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(name=pdf_output.name)

    # Send PDF
    with open(pdf_output.name, "rb") as file:
        line_bot_api.push_message(
            user_id,
            FileMessage(original_content_url=f"{os.environ['BASE_URL']}/files/{pdf_output.name}", file_name="translated.pdf")
        )

@app.route("/files/<path:path>", methods=["GET"])
def serve_file(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    app.run()
