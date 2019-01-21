# Web Crawler

A simple web crawler which visits all pages within the domain, but does not follow the links to external sites such as Google or Twitter.

The output is a simple structured site map, showing links to other pages under the same domain, links to external URLs and links to static content such as images for each respective page.

## How to run the crawler

```
python3 crawler.py starting-url [max-depth]
```

Arguments:
- `starting-url` - the starting URL, for example `http://google.com`
- `max-depth` - (optional argument, integer) follow the link only if it is `max-depth` or fewer levels below the starting URL

The crawler outputs a simple site map to the standard output.

## Assumptions

- The starting URL is a full domain (for example `http://google.com`) and not a URL with a path (for example
  `http://google.com/privacy`).
- I only used built-in Python libraries.
- I interpreted "links to images" as just "images" (under tag `img`). The implementation could be modified to handle
  links to images and other static content.
- URLs discovered in the webpage are output as they are provided in the source of the website (relative URLs and
  anchors are not resolved in the output).
- URLs which are followed are standardized: they are all accessed with HTTP (and not HTTPS), relative URLs are converted
  to absolute URLs. The goal of the standardization it to visit each page only once (I assume that HTTP and HTTPS
  lead to the same website. This does not have to be true, but it's usually the case).


