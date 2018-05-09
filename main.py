import requests

def fetchandwritetofile(url):
    result = requests.get(url).json()
    messages = result['data']
    for message in messages :
        if 'message' not in message:
            continue
        confession = message['message'].encode('utf-8').strip()
        if len(confession) <= 100:
            shortConfession = str.replace(confession,'\n',' ').split(' ', 1)
            if len(shortConfession) < 2:
                continue
            file.write(shortConfession[1]+'\n')
        print message['message']
    if 'paging' not in result or 'next' not in result['paging']:
        return
    nextUrl = result['paging']['next']
    fetchandwritetofile(nextUrl)



filename = 'atudahconfessions.txt'

#atudahconfessions.txt
#courseconfessions.txt
#gimelconfessions.txt
#idfconfessions.txt
#lotemconfessions.txt
#magavconfessions.txt
file = open(filename, 'w')
#magav = 1983142491936079
# idf = 332027507300337
#atudah = 103700257119156
#gimelim = 541722549557331
#course = 934125433435325
#lotem = 1797168187012385
# TODO: the url is valid for a certain period of time be sure to recheck if needed
uu = "https://graph.facebook.com/v2.6/103700257119156/posts?limit=100&access_token=EAACEdEose0cBANkyrQ9RLdA1WzLcn6UhpqjMHDmAzBKlKbC8VYLOloshBuwzQZCDhdsJG93AzYFSDwaIMGeXS6qgTaaZBp3ffZBZCMEnTthzMK5XNhqfymGN88RIN0Bq9kzklRWNxAqZAehWUyN4Az047H42oaSnSrZC7WrvoirqAaewTLge6jiOyUeXFThxgZD"
fetchandwritetofile(uu)
file.close()
print readFromFile(filename)


