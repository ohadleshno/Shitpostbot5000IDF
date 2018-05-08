# coding=utf-8
import io
from multiprocessing import Pool
import requests
from meme.generator import Memegen
import urllib


class BotHandler:
    def __init__(self, token):
        self.messages_to_send = []
        self.offset = None
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        if len(result_json) != 0:
            print 'add new messeges'
            self.messages_to_send.extend(result_json)
            self.offset = result_json[-1]['update_id'] + 1
        return len(result_json)

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_image(self, chat_id):
        files = {'photo': open('/path/to/img.jpg', 'rb')}
        data = {'chat_id': chat_id}
        r = requests.post(self.api_url + "sendPhoto", files=files, data=data)
        print(r.status_code, r.reason, r.content)
        return r

    def send_image_remote_file(self, img_url, chat_id):
        remote_image = requests.get(img_url)
        photo = io.BytesIO(remote_image.content)
        photo.name = 'img.png'
        files = {'photo': photo}
        data = {'chat_id': chat_id}
        r = requests.post(self.api_url + "sendPhoto", files=files, data=data)
        print(r.status_code, r.reason, r.content)
        return r

    def get_last_update(self):
        if len(self.messages_to_send) != 0:
            message = self.messages_to_send.pop()
            print "start generating receiving for message {}".format(message)
            return message


greet_bot = BotHandler('531246614:AAHec96fLxTRBJg8XiJmwhahkcicY1G2KGc')
greetings = ('hello', 'hi', 'greetings', 'sup', 'שלום', 'מה נשמע', 'מה הולך', 'היי')
memegen = Memegen()


def send_meme(last_update):
    last_chat_text = last_update['message']['text'].encode('UTF-8')
    print "received text {}".format(last_chat_text)

    last_chat_id = last_update['message']['chat']['id']

    if last_chat_text.lower() == "/start":
        last_chat_name = last_update['message']['chat']['first_name']
        welcomeMessage = 'Hi {} welcome to mahanet 2018 shitpostbotidf5000. Send message and you will receive meme.'
        greet_bot.send_message(last_chat_id,
                               welcomeMessage.format(
                                   last_chat_name))
    else:
        print "started generating meme {}".format(last_chat_text)
        text_in_utf = last_chat_text.decode('utf-8')
        url = memegen.generate("", text_in_utf)
        greet_bot.send_image_remote_file(
            url,
            last_chat_id)
        print "finished sending meme".format(last_chat_text)


def main():
    pool = Pool(processes=10)  # Start a worker processes.

    while True:
        greet_bot.get_updates()
        last_update = greet_bot.get_last_update()
        if last_update != None:
            pool.apply_async(send_meme, [last_update])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
