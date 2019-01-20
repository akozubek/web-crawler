import urllib.request
import sys

def usage():
    print('Usage: python3 crawler.py starting-url')

def download(url):
    print('Downloading', url)
    response = urllib.request.urlopen(url)
    data = response.read()
    return data

def main(): 
    if len(sys.argv) <= 1:
        usage()
        exit(1)

    # Arguments provided -> continue with download 
    page = download(sys.argv[1])

if __name__ == "__main__":
    main()
