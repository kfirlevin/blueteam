import requests
from dotenv import load_dotenv
import os


env_path = os.path.expanduser('~/telebot/.env')

load_dotenv(dotenv_path=env_path)

url = "https://api.telegram.org/{}/sendMessage?chat_id={}&text={}"


print(os.getenv("BOT_KEY"))


def sendMessage(message):
    requests.get(url.format(os.getenv("BOT_KEY"),
                            os.getenv("CHAT_NAME"), message))


if __name__ == "__main__":
    sendMessage('How are ya?')
