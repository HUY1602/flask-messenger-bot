from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'huy1602')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN', 'your_page_access_token')

@app.route('/')
def home():
    return 'Hello, this is your Flask bot!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Token mismatch", 403

    if request.method == 'POST':
        data = request.get_json()
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:
                    sender_id = messaging_event['sender']['id']
                    if messaging_event.get('message'):
                        message_text = messaging_event['message'].get('text')
                        reply(sender_id, f"Bạn vừa nói: {message_text}")
        return "ok", 200

def reply(recipient_id, text):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    auth = {'access_token': PAGE_ACCESS_TOKEN}
    requests.post('https://graph.facebook.com/v17.0/me/messages',
                  params=auth, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
