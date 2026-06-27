import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_catalog():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Let's just print all the text or a sample of links to see what we're dealing with
    links = soup.find_all('a')
    valid_links = []
    for a in links:
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if href and text:
            valid_links.append((text, href))
            
    print(f"Found {len(valid_links)} links.")
    for text, href in valid_links[:20]:
        print(f"{text}: {href}")

if __name__ == "__main__":
    scrape_catalog()
