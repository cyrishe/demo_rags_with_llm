import requests


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}

search_url= 'https://www.googleapis.com/customsearch/v1?key=AIzaSyBoFyMXXmQjuwrO36OMO68aYJFUYEwPVUk&cx=3305384ea63714692&q='

def search_google(query):
    url = search_url +query
    response = requests.get(url, headers=headers).text
    return response



def pick_result(response):

if __name__ == '__main__':
    res = search_google('康定医疗')
    print(res)
