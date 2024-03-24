import requests
from bs4 import BeautifulSoup
import random
import time
import os

def get_random_user_agent():
  user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.64 Mobile Safari/537.36"
    
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_11_5) Gecko/20100101 Firefox/72.9"
    "Mozilla/5.0 (Windows; Windows NT 10.5; Win64; x64; en-US) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/47.0.3194.374 Safari/603.1 Edge/15.92793"
    "Mozilla/5.0 (Windows; U; Windows NT 10.5;; en-US) AppleWebKit/601.7 (KHTML, like Gecko) Chrome/49.0.2867.180 Safari/600.2 Edge/14.47322"
    "Mozilla/5.0 (Windows; Windows NT 10.1; x64; en-US) AppleWebKit/601.7 (KHTML, like Gecko) Chrome/53.0.2505.129 Safari/537"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_5_1; like Mac OS X) AppleWebKit/536.14 (KHTML, like Gecko)  Chrome/50.0.1911.252 Mobile Safari/603.7"
    "Mozilla/5.0 (U; Linux x86_64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/54.0.2922.318 Safari/603"
    "Mozilla/5.0 (U; Linux i673 ) AppleWebKit/533.49 (KHTML, like Gecko) Chrome/55.0.1625.229 Safari/600"
    "Mozilla/5.0 (Windows; U; Windows NT 10.1; WOW64) Gecko/20100101 Firefox/72.7"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_3_7; like Mac OS X) AppleWebKit/602.24 (KHTML, like Gecko)  Chrome/52.0.2106.328 Mobile Safari/601.5"
    
  ]
  return random.choice(user_agents)

def random_delay():
  # Adjust the range as needed (in seconds)
  delay = random.uniform(2, 5)  # Delay between 2 and 5 seconds
  time.sleep(delay)

def scrape_images(url, target_folder):
  headers = {"User-Agent": get_random_user_agent()}

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")

    # Create the target folder with subdirectories if needed
    os.makedirs(target_folder, exist_ok=True)

    for image in images:
      image_url = image.get("src")
      if image_url and image_url.startswith("http"):  # Ensure a valid, absolute URL
        filename = os.path.basename(image_url)
        filepath = os.path.join(target_folder, filename)

        try:
          random_delay()  # Introduce random delay before each request
          image_response = requests.get(image_url, headers=headers)
          image_response.raise_for_status()

          with open(filepath, "wb") as f:
            f.write(image_response.content)
          print(f"Image saved: {filename}")

        except requests.exceptions.RequestException as e:
          print(f"Error downloading {image_url}: {e}")

  except requests.exceptions.RequestException as e:
    print(f"Error fetching website: {e}")

if __name__ == "__main__":
  target_url = input("Enter the URL to scrape images from: ")
  target_dir = input("Enter the full path of the directory to create the folder in: ")
  folder_name = input("Enter the name of the folder to create within the directory: ")
  target_folder = os.path.join(target_dir, folder_name)  # Join path components
  scrape_images(target_url, target_folder)
