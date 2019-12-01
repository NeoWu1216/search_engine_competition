from bs4 import BeautifulSoup
import urllib.request


def get_info():
    req = urllib.request.Request('http://cs510-search.centralus.cloudapp.azure.com/')
    response = urllib.request.urlopen(req).read()

    soup = BeautifulSoup(response, 'html.parser')
    # print(soup.prettify())

    for tr in soup.find_all('tr'):
        tds = list(map(lambda x:x.text, tr.find_all('td')))
        if 'null' in tds:
            return tds

if __name__ == '__main__':
    print(get_info())