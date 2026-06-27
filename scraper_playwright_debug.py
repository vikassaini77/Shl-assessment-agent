from playwright.sync_api import sync_playwright
import json

def scrape_shl_catalog():
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.shl.com/solutions/products/product-catalog/", timeout=60000)
        
        # Wait for the catalog to load.
        page.wait_for_timeout(5000)
        
        # Try to extract the HTML to see what elements are present
        html = page.content()
        with open("catalog_playwright.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        print("HTML saved to catalog_playwright.html")
        browser.close()

if __name__ == "__main__":
    scrape_shl_catalog()
