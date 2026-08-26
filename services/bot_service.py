import urllib.parse
import urllib.request

from config import Config


class BotService:
    def __init__(self):
        self.token = Config.BOT_TOKEN
        self.chat_id = Config.CHAT_ID

    def send_message(self, text):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = urllib.parse.urlencode({
                "chat_id": self.chat_id,
                "text": text
            }).encode()

            urllib.request.urlopen(url, data=data)

        except Exception as e:
            print("Bot error:", e)

    def notify_new_user(self, username):
        self.send_message(f"New user registered: {username}")

    def notify_admin_action(self, action, detail):
        self.send_message(f"Admin action: {action}. Detail: {detail}")