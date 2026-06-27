import requests

def save_catalog():
    url = "https://www.shl.com/solutions/products/product-catalog/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    with open('catalog_correct.html', 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    save_catalog()
