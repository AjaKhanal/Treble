from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def find_url(label):
    page_url = "https://www.youtube.com/results?search_query=" + label.replace(" ", "+")

    print(page_url)

    req = Request(page_url, headers={'User-Agent': 'XYZ/3.0'})
    response = urlopen(req, timeout=20).read()

    page_soup = soup(response, "html.parser")
    # TODO
    # fix this line
    containers = page_soup.findAll('a', {'class': 'pl-video-title-link'})

    data = []
    for container in containers:
        data.append(container.get('href'))

    return data



