import requests

def fetchandwritetofile(url):
    result = requests.get(url).json()
    messages = result['posts']['data']
    for message in messages :
        file.write(message['message'].encode('utf-8').strip()+'\n')
        print message['message']
    if 'paging' not in result:
        return
    nextUrl = result['paging']['next']
    fetchandwritetofile(nextUrl)



filename = 'magavconfessions.txt'
file = open(filename, 'w')

# TODO: the url is valid for a certain period of time be sure to recheck if needed
uu = "https://graph.facebook.com/v2.6/1983142491936079?fields=posts.limit(100)&access_token=EAACEdEose0cBABA8VUNzolwRkPG373uU9r708Dq3d6VsJi4nhxUDnvdXGtGY9IZB2kkQ3xpoBfKWzZC1rJPjDm1RcBrocsAlAANM7FiOXVBbKORrf63Yq84SRmHQSVTKwHT7oAPbIN9Qe5QVPkcZCzrNljJ9ZAdvZBdxGOe2Rct4ICclhgEuqmJL1KtmTVR4ZD"
fetchandwritetofile(uu)
file.close()
print readFromFile(filename)


