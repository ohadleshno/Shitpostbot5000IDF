import requests

def fetchandwritetofile(url):
    result = requests.get(url).json()
    messages = result['data']
    for message in messages :
        file.write(message['message'].encode('utf-8').strip()+'\n')
        print message['message']
    if 'paging' not in result:
        return
    nextUrl = result['paging']['next']
    fetchandwritetofile(nextUrl)



filename = 'idfconfessions.txt'
file = open(filename, 'w')

# TODO: the url is valid for a certain period of time be sure to recheck if needed
uu = "https://graph.facebook.com/v2.6/332027507300337/posts?limit=100&access_token=EAACEdEose0cBAFZA9RPtdOgt7MsZCFFe8dVealI1bHZBjiHBzOtU6gMnWD3xvrfBZAQ0MsamuiFIo8r4MvnK1CjNFb6NnZBZCBxdD2cGgAj93tQMLEUbNuZA6XVITaDjxNolANpTYrZAYE4LgjU9a9GIthrbK1vFC4taLrpxJJ1ZC5ywqDhW4RAZCuilBjyoEA9zQZD"
fetchandwritetofile(uu)
file.close()
print readFromFile(filename)


