import urllib.request
from urllib.parse import urlparse
import sys
from html.parser import HTMLParser

class WebCrawlerParser(HTMLParser):
    def __init__(self, domain):
        HTMLParser.__init__(self) 
        self.domain = domain
        self.external_urls = set()
        self.internal_urls = set()
        self.images = set()
    
    def _get_attr(self, attrs, name):
        for n, v in attrs:
             if n == name:
                  return v
        return None

    def _is_internal(self, url):
        parsed_url = urlparse(url) 
        return parsed_url.netloc == self.domain or parsed_url.netloc == ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = self._get_attr(attrs, 'href')
            if href is None:
                return
            if self._is_internal(href):
                self.internal_urls.add(href)
            else: 
                self.external_urls.add(href)
        if tag == 'img':
            src = self._get_attr(attrs, 'src')
            if src is None:
                return
            self.images.add(src)

    def get_images(self):
        return self.images

    def get_external_urls(self):
        return self.external_urls

    def get_internal_urls(self):
        return self.internal_urls

def usage():
    print('Usage: python3 crawler.py starting-url')

def download(url):
    try: 
        response = urllib.request.urlopen(url)
    except Exception as e:
        print('Downloading from url', url, 'failed. Details:', str(e))
        exit(1)
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
    domain = urlparse(url).netloc
    parser = WebCrawlerParser(domain)
    parser.feed(str(page))
    print_info('Internal URLs: ', parser.get_internal_urls())
    print_info('External URLs: ', parser.get_external_urls())
    print_info('Images: ', parser.get_images())

if __name__ == "__main__":
    main()
