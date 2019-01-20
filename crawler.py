import urllib.request
import sys
from html.parser import HTMLParser

class WebCrawlerParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self) 
        self.images = set()
        self.urls = set()
    
    def _get_attr(self, attrs, name):
        for n, v in attrs:
             if n == name:
                  return v
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = self._get_attr(attrs, 'href')
            self.urls.add(href)
        if tag == 'img':
            src = self._get_attr(attrs, 'src')
            self.images.add(src)

    def get_images(self):
        return self.images

    def get_urls(self):
        return self.urls

def usage():
    print('Usage: python3 crawler.py starting-url')

def download(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data

def print_info(header, items):
    print(header)
    for element in sorted(items):
        print('\t', element)

def main(): 
    if len(sys.argv) <= 1:
        usage()
        exit(1)

    # Arguments provided -> continue with download 
    url = sys.argv[1]
    print('Downloading', url)
    page = download(url)
    print('Parsing downloaded page')
    parser = WebCrawlerParser()
    parser.feed(str(page))
    print_info('Links: ', parser.get_urls())
    print_info('Images: ', parser.get_images())

if __name__ == "__main__":
    main()
