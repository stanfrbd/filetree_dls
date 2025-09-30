import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse, unquote
import time
import os
import logging
from datetime import datetime

proxy = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(os.path.dirname(__file__), f"filetree_{timestamp}.txt")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def inject_token(url, token):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["token"] = [token]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def extract_path(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    raw_path = params.get("path", [""])[0]
    return unquote(raw_path)

def fetch_links(base_url, url, visited, token, depth=0):
    if url in visited:
        return

    visited.add(url)
    path = extract_path(url)
    indent = "  " * depth
    logging.info(f"{indent}- {path or '/'}")

    try:
        response = requests.get(url, proxies=proxy)
        if response.status_code != 200:
            logging.info(f"{indent}  [HTTP Error {response.status_code}]")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]

        for link in links:
            link_with_token = inject_token(link, token)
            if link_with_token.startswith(base_url) and link_with_token not in visited:
                fetch_links(base_url, link_with_token, visited, token, depth + 1)

    except requests.exceptions.RequestException as e:
        logging.info(f"{indent}  [Network Exception] {e}")

start_url = "http://example.onion/dls"

parsed_start = urlparse(start_url)
query_params = parse_qs(parsed_start.query)
token = query_params.get("token", [""])[0]

base_url = parsed_start._replace(query="").geturl()
visited_urls = set()
fetch_links(base_url, start_url, visited_urls, token)
