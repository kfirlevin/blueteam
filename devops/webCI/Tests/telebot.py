import requests
from dotenv import load_dotenv
import os
import datetime


env_path = os.path.expanduser('/telebot/.env')

load_dotenv(dotenv_path=env_path)

url = "https://api.telegram.org/{}/sendMessage?chat_id={}&text={}"


def sendMessage(message):

    requests.get(url.format(os.getenv("BOT_KEY"),
                            os.getenv("CHAT_NAME"), message))


def parse_files(providers, weight):
    try:
        with open(providers, "r") as provfile:
            content = provfile.read()
            sendMessage(
                'Providers Test start - {}\n'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            sendMessage(content)
            sendMessage('Providers Test end ############################\n')
        with open(weight, "r") as provfile:
            content = provfile.read()
            sendMessage(
                'Weight Test start - {}\n'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            sendMessage(content)
            sendMessage('Weight Test end ############################\n')
    except IOError as error:
        pass


if __name__ == "__main__":
    sendMessage('How are ya?')
