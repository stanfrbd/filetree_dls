import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

proxy = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

def fetch_links(base_url, url, visited):
    if url in visited:
        return  # Prevent revisiting the same page

    visited.add(url)
    print(url)  # Output the current page

    try:
        response = requests.get(url, proxies=proxy)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]

        for link in links:
            # Ensure the link remains within the base folder
            if link.startswith(base_url) and link not in visited:
                #time.sleep(2)  # Add delay if needed
                fetch_links(base_url, link, visited)  # Recursive call

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

# Set base folder for enumeration
base_url = "http://example.onion/dls"
visited_urls = set()
fetch_links(base_url, base_url, visited_urls)
 
