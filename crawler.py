import urllib.request
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import urlunsplit
from urllib.parse import urljoin
from urllib.parse import ParseResult
import sys
from html.parser import HTMLParser
from collections import namedtuple

WebsiteInfo = namedtuple('WebsiteInfo', ['internal_urls', 'external_urls', 'images'])

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
                  if v.startswith('\\\'') and v.endswith('\\\''):
                     return v.replace('\\\'', '').replace('\\\'','')	
                  else: 
                     return v
        return None

    def _is_internal_link(self, url):
        parsed_url = urlparse(url) 
        is_same_domain = (parsed_url.netloc == self.domain or parsed_url.netloc == '')
        return is_same_domain

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = self._get_attr(attrs, 'href')
            if href is None:
                return
            if self._is_internal_link(href):
                self.internal_urls.add(href)
            else: 
                self.external_urls.add(href)
        if tag == 'img':
            src = self._get_attr(attrs, 'src')
            if src is None:
                return
            self.images.add(src)

    def get_website_info(self):
        return WebsiteInfo(self.internal_urls, self.external_urls, self.images)

def usage():
    print('Usage: python3 crawler.py starting-url max-depth')

def download(url):
    try: 
        response = urllib.request.urlopen(url)
    except Exception as e:
        print('Downloading from url', url, 'failed. Details:', str(e))
        exit(1)
    data = response.read()
    return data

def print_website_single_info(header, items):
    print('\t', header)
    for element in sorted(items):
        print('\t\t', element)

def print_website_info(website_info):
    print_website_single_info('Internal URLs: ', website_info.internal_urls)
    print_website_single_info('External URLs: ', website_info.external_urls)
    print_website_single_info('Images: ', website_info.images)

def print_info(websites):
    for website in sorted(websites.keys()):
        print(website)
        print_website_info(websites[website])

def standardize_url(url, domain):
    parsed_url = urlparse(url)
    # Relative URL -> convert to absolute
    if parsed_url.netloc == '':
        url = urljoin('http://'+domain, url)
        parsed_url = urlparse(url)

    path = parsed_url.path
    if path == '' or not parsed_url.path.endswith('/'):
        path = path + '/'

    # https: change to http
    url = urlunsplit(('http', parsed_url.netloc, path, '', ''))
    return url

def is_link(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ('http', 'https')


def crawl_website(starting_url, domain, websites, current_depth, max_depth = 0):
    print('Downloading', starting_url)
    page = download(starting_url)

    parser = WebCrawlerParser(domain)
    parser.feed(str(page))
    website_info = parser.get_website_info()
    websites[starting_url] = website_info
   
    if current_depth < max_depth:
        for internal_url in website_info.internal_urls:
            standard_url = standardize_url(internal_url, domain)
            if is_link(standard_url) and standard_url not in websites.keys():
                crawl_website(standard_url, domain, websites, current_depth+1, max_depth)


def main(): 
    if len(sys.argv) <= 2:
        usage()
        exit(1)

    # Arguments provided -> continue with download 
    url = sys.argv[1]
    max_depth = int(sys.argv[2])
    domain = urlparse(url).netloc
    url = standardize_url(url, domain)
    websites = dict()
    crawl_website(url, domain, websites, 0, max_depth)
    print_info(websites)

if __name__ == "__main__":
    main()
