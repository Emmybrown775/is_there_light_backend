import os

from flask import Flask, request
import requests
app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = os.environ.get('CHAT_ID')

tel_response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/setWebhook",
    json={"url": f"https://is-there-light-backend.onrender.com/{TOKEN}"}
)

@app.route(f'/{TOKEN}', methods=['POST'])
def bot_webhook():  # put application's code here
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        print(chat_id)

        if text == "/start":
            send_message(chat_id, "Welcome Emmy. If you're not me, politely fuck off")

        elif text == "/check":
            response = requests.get("http://192.168.251.140/data")
            status = response.json()["status"]

            if status == "on":
                send_message(chat_id, "There is still light boss, relax.")
            else :
                send_message(chat_id, "Where you see light?? Why you dey check, abeg stop disturbing the server.")

    return "ok", 200


@app.route("/update", methods=["POST"])
def update():
    request_data = request.get_json()

    status = request_data["status"]
    if status == "on":
        send_message(CHAT_ID, "UP NEPAAAAAA!!!!!!!!!!!!!")
    elif status == "off":
        send_message(CHAT_ID, "TINUBUUUUUUUUUU!!!!!!!!!!!!!!")



def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run()
