import random
import requests


class Memegen:

    def __init__(self):
        random.seed(123932)
        self.BASE_URL = "https://memegen.link"
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
            link = "https://memegen.link/{}/your-text/goes-here.jpg".format(alias)

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
        path = "/{0}/{1}/{2}.jpg".format(template, top or '_', bottom or '_')

        if alt:
            path += "?alt={}".format(alt)

        url = self.BASE_URL + path

        return url

    def generate(self, top, bottom):
        return self.build_url(self.valid_templates[random.randint(0, len(self.valid_templates) - 1)].decode('UTF-8'), top, bottom)


def image_exists(path):
    if path.split("://")[0] not in ["http", "https"]:
        return False

    r = requests.head(path)
    return r.status_code == requests.codes.ok