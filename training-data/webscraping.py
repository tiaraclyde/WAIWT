import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download an image from a URL
def download_image(url, folder, count):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_filename = os.path.join(folder, f"image_{count}.jpg")
        img.save(img_filename)
        print(f"Downloaded: {img_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Function to scrape Pinterest for a given style
def scrape_pinterest_style(style, folder, min_images=50):
    search_url = f"https://www.pinterest.com/search/pins/?q={style}"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(search_url)
    scroll_pause_time = 2  # Pause to allow images to load
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    img_urls = set()
    
    while len(img_urls) < min_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tags = soup.find_all('img', {'src': True})
        
        for img_tag in img_tags:
            img_url = img_tag['src']
            if img_url.startswith('http'):
                img_urls.add(img_url)
            if len(img_urls) >= min_images:
                break
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    driver.quit()
    
    create_directory(folder)
    
    # Download images
    for count, img_url in enumerate(img_urls):
        if count >= min_images:
            break
        download_image(img_url, folder, count)

def main():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    styles = ["clean girl aesthetic", "stockholm style", "cottagecore aesthetic style", "alt aesthetic style", "streetstyle outfits", "preppy style outfits"]
    
    for style in styles:
        folder_path = os.path.join(base_folder, style.replace(" ", "_"))
        scrape_pinterest_style(style, folder_path)

if __name__ == "__main__":
    main()