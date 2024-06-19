#command line: pip3 install requests beautifulsoup4 pillow selenium webdriver-manager
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, folder, count):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_filename = os.path.join(folder, f"image_{count}.jpg")
        img.save(img_filename)
        print(f"Downloaded: {img_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_pinterest_style(style, folder, max_images=100):
    search_url = f"https://www.pinterest.com/search/pins/?q={style}"
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(search_url)
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all('img', {'src': True})
    
    create_directory(folder)
    
    for count, img_tag in enumerate(img_tags):
        if count >= max_images:
            break
        img_url = img_tag['src']
        if img_url.startswith('http'):
            download_image(img_url, folder, count)
    
    driver.quit()

def main():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    styles = ["clean girl aesthetic style inspo", "stockholm style inspo", "cottagecore style inspo", "alt style inspo", "streetstyle inspo", "preppy style inspo"]
    
    for style in styles:
        folder_path = os.path.join(base_folder, style.replace(" ", "_"))
        scrape_pinterest_style(style, folder_path)

if __name__ == "__main__":
    main()