# coding=utf-8
import random
import requests
import urllib


class Memegen:
    def __init__(self):
        random.seed(123932)
        self.BASE_URL = "http://localhost:5000"
        self.template_info = self.get_template_info()
        self.valid_templates = self.get_valid_templates()
        self.template_list = self.get_template_list()

    def get_valid_templates(self):
        return [x[0] for x in self.template_info]

    def get_template_info(self):
        template = requests.get(self.BASE_URL + "/api/templates/").json()

        data = []

        for description, api_link in template.items():
            alias = api_link.split("/api/templates/")[1]
            link = "https://memegen.link/{}/your-text/goes-here.jpg?font=mplus-2p-black".format(alias)

            alias = alias.encode('utf8')
            description = description.encode('utf8')
            link = link.encode('utf8')

            data.append((alias, description, link))

        return sorted(data, key=lambda x: x[0])

    def get_template_list(self):
        help = ""

        for alias, description, example_link in self.template_info:
            help += '`<{}|{}>` {}\n'.format(example_link, alias, description)

        return help

    def build_url(self, template, top, bottom, alt=None):
        new_top = ""
        new_bottom = bottom

        if len(bottom) > 20:
            words = bottom.split()
            new_bottom = " ".join(words[:4])
            new_top = " ".join(words[4:])

        path = "/{0}/{1}/{2}.jpg?font=mplus-2p-black".format(template, urllib.quote(new_top.encode('utf8')) or '_',
                                                             urllib.quote(new_bottom.encode('utf8')) or '_')

        if alt:
            path += "?alt={}".format(alt)

        url = self.BASE_URL + path

        return url

    # -*- coding: utf-8 -*-
    def isAllEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def generate(self, top, bottom):
        if not self.isAllEnglish(top):
            top = top[::-1]
        if not self.isAllEnglish(bottom):
            bottom = bottom[::-1]

        return self.build_url(self.valid_templates[random.randint(0, len(self.valid_templates) - 1)].decode('UTF-8'),
                              top, bottom)


def image_exists(path):
    if path.split("://")[0] not in ["http", "https"]:
        return False

    r = requests.head(path)
    return r.status_code == requests.codes.ok
