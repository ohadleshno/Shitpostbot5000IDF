# coding=utf-8
import io
import json
from multiprocessing import Pool

import requests

from meme.generator import Memegen

# from telegram import InlineKeyboardButton

filename = 'idfconfessions.txt'
liked = []
no_liked = []
message_to_url = {}
message_url_tuples = []


class BotHandler:
    def __init__(self, token):
        # self.confessions = self.readFromFile(fname)
        self.inline_keyboard = [[
            {'text': 'אהבתי', 'callback_data': 'like'},
            {'text': 'נסה שוב', 'callback_data': 'retry'}]]
        self.messages_to_send = []
        self.callback_messages = []
        self.offset = None
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.confessions = []
        try:
            self.confessions = self.readFromFile('allconfessions.txt')
        except Exception:
            print("Error: Could not read all confesions file!!!!!")

    def readFromFile(self, fname):
        with open(fname) as f:
            return f.readlines()

    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        if len(result_json) != 0:
            print 'add new messeges'

            for result in result_json:
                if u'callback_query' not in result:
                    self.messages_to_send.append(result)
                else:
                    self.callback_messages.append(result['callback_query'])

            self.offset = result_json[-1]['update_id'] + 1

        return len(result_json)

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def recived_send_message(self, chat_id):
        params = {'chat_id': chat_id, 'limit': 1}
        method = 'getHistory'
        resp = requests.get(self.api_url + method, params)
        print resp
        return resp

    def send_image(self, chat_id):
        files = {'photo': open('/path/to/img.jpg', 'rb')}
        data = {'chat_id': chat_id, 'reply_markup': {'inline_keyboard': self.inline_keyboard}}
        r = requests.post(self.api_url + "sendPhoto", files=files, data=data)
        print(r.status_code, r.reason, r.content)
        return r

    def build_keyboard(self, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def send_image_remote_file(self, img_url, chat_id):
        global message_url_tuples
        remote_image = requests.get(img_url)
        photo = io.BytesIO(remote_image.content)
        photo.name = 'img.png'
        files = {'photo': photo}
        data = {'chat_id': chat_id, 'parse_mode': 'Markdown',
                'reply_markup': json.dumps({'inline_keyboard': self.inline_keyboard})}
        r = requests.post(self.api_url + "sendPhoto", files=files, data=data)
        message_to_url[r.json()['result']['message_id']] = img_url
        message_url_tuples.append((r.json()['result']['message_id'], img_url))
        with open('imgid2url/{}.txt'.format(r.json()['result']['message_id']), 'w') as f:
            f.write(img_url)
        print(r.status_code, r.reason, r.content)
        return r

    def get_last_update(self):
        if len(self.messages_to_send) != 0:
            message = self.messages_to_send.pop()
            print "start generating receiving for message {}".format(message)
            return message

    def get_last_callback(self):
        if len(self.callback_messages) != 0:
            return self.callback_messages.pop()


greet_bot = BotHandler('531246614:AAHec96fLxTRBJg8XiJmwhahkcicY1G2KGc')
greetings = ('hello', 'hi', 'greetings', 'sup', 'שלום', 'מה נשמע', 'מה הולך', 'היי')
memegen = Memegen()


def send_meme(last_update):
    last_chat_text = last_update['message']['text'].encode('UTF-8')
    print "received text {}".format(last_chat_text)

    last_chat_id = last_update['message']['chat']['id']
    print "last chat id {}".format(last_chat_id)

    if last_chat_text.lower() == "/start":
        last_chat_name = last_update['message']['chat']['first_name']
        welcomeMessage = 'שלום {} ברוך הבא לבוט מגנרט ממים צהליים 5000. הקלד משפט ונגרט לך מם מותאם למשפט'
        greet_bot.send_message(last_chat_id,
                               welcomeMessage.format(
                                   last_chat_name))
    else:
        print "started generating meme {}".format(last_chat_text)
        text_in_utf = last_chat_text.decode('utf-8')
        if "וידוי" in text_in_utf:
            #TODO add confessions
            greet_bot.send_message(last_chat_id, memegen.confessions[0])
        else:
            url = memegen.generate("", text_in_utf)
            greet_bot.send_image_remote_file(
                url,
                last_chat_id)
        print "finished sending meme".format(last_chat_text)


def send_callback_message(last_callback):
    last_chat_id = last_callback['message']['chat']['id']
    print 'sending callback message for chat_id {}'.format(last_chat_id)
    last_chat_text = last_callback['data'].encode('utf8')

    if last_chat_text.lower() in ['like']:
        greet_bot.recived_send_message(last_chat_id)
        liked.append(last_callback['message']['message_id'])
        greet_bot.send_message(last_chat_id, "תודה רוצה עוד אחד? הקלד עוד משפט")
    elif last_chat_text.lower() == 'retry':
        no_liked.append(last_callback['message']['message_id'])
        greet_bot.send_message(last_chat_id, "לא נורא נסה עוד פעם. הקלד עוד משפט")


def print_liked_and_unliked():
    global liked, no_liked
    if (len(liked) >= 20):
        liked_urls = []
        for i in liked:
            with open('imgid2url/{}.txt'.format(i), 'r') as f:
                liked_urls.append(f.read())
        with open('like.txt', 'a') as f:
            f.write('\n'.join(liked_urls) + '\n')
        liked = []

    if (len(no_liked) >= 20):
        dis_liked_urls = []
        for i in liked:
            with open('imgid2url/{}.txt'.format(i), 'r') as f:
                dis_liked_urls.append(f.read())
        with open('unlike.txt', 'a') as f:
            f.write('\n'.join(dis_liked_urls) + '\n')
        no_liked = []

def main():
    global message_url_tuples
    pool = Pool(processes=10)  # Start a worker processes.

    while True:
        greet_bot.get_updates()
        last_update = greet_bot.get_last_update()
        if last_update != None:
            pool.apply_async(send_meme, [last_update])
        last_callback = greet_bot.get_last_callback()
        if last_callback != None:
            send_callback_message(last_callback)

        print_liked_and_unliked()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
