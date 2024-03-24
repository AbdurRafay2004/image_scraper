import requests
from bs4 import BeautifulSoup
import os

def scrape_images(url, target_folder="images"):
    """Scrapes images from the given URL and saves them to the target folder."""

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("img")

        os.makedirs(target_folder, exist_ok=True)  # Create the folder if it doesn't exist

        for image in images:
            image_url = image.get("src")
            if image_url and image_url.startswith("http"):  # Ensure a valid, absolute URL
                filename = os.path.basename(image_url)
                filepath = os.path.join(target_folder, filename)

                try:
                    image_response = requests.get(image_url)
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
    scrape_images(target_url)
