# coding=utf-8
import io
from multiprocessing import Pool

import requests
from meme.generator import Memegen


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_image(self, chatId):
        files = {'photo': open('/path/to/img.jpg', 'rb')}
        data = {'chat_id': chatId}
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
        print "trying to get new message"
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            print len(get_result)
            last_update = get_result[len(get_result)]

        print "finished receiving new message {}".format(last_update)
        return last_update


greet_bot = BotHandler('531246614:AAHec96fLxTRBJg8XiJmwhahkcicY1G2KGc')
greetings = ('hello', 'hi', 'greetings', 'sup', 'שלום', 'מה נשמע', 'מה הולך', 'היי')
memegen = Memegen()


def send_meme(last_update):
    last_chat_text = last_update['message']['text']
    print "received text {}".format(last_chat_text)

    last_chat_id = last_update['message']['chat']['id']

    if last_chat_text.lower() == "/start":
        last_chat_name = last_update['message']['chat']['first_name']
        welcomeMessage = 'Hi {} welcome to mahanet 2018 shitpostbotidf5000. Send message and you will receive meme.'
        greet_bot.send_message(last_chat_id,
                               welcomeMessage.format(
                                   last_chat_name))
    else:
        text_in_utf = last_chat_text.encode('UTF-8')
        print "started generating meme {}".format(last_chat_text)
        greet_bot.send_image_remote_file(
            memegen.generate("", text_in_utf),
            last_chat_id)
        print "finished sending meme".format(last_chat_text)


def print_finish():
    print 'finish';


def main():
    new_offset = None
    pool = Pool(processes=10)  # Start a worker processes.

    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        last_update_id = last_update['update_id']
        send_meme(last_update)
        pool.apply_async(send_meme, [last_update],
                                  print_finish)  # Evaluate "f(10)" asynchronously calling callback when finished.

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
