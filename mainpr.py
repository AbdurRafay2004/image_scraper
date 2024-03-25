import requests
from bs4 import BeautifulSoup
import random
import os


def read_headers_from_file(filename):
  """Reads a list of headers from a text file."""
  headers_list = []
  with open(filename, "r") as f:
    for line in f:
      line = line.strip()  # Remove leading/trailing whitespace
      if line and not line.startswith("#"):  # Skip comments and empty lines
        headers = {}
        for header_line in line.splitlines():  # Split header lines if multi-line
          key, value = header_line.split(":", 1)  # Separate key-value pairs
          headers[key.strip()] = value.strip()
        headers_list.append(headers)
  return headers_list


def read_excluded_patterns_from_file(filename):
  """Reads a list of excluded URL patterns from a text file."""
  excluded_patterns = []
  with open(filename, "r") as f:
    for line in f:
      pattern = line.strip()  # Remove leading/trailing whitespace and comments
      if pattern:
        excluded_patterns.append(pattern)
  return excluded_patterns


def scrape_images(url, target_folder, excluded_patterns_file):
  headers = read_headers_from_file("header_list.txt")  # Load headers from file
  random_headers = random.choice(headers)  # Select a random header
  excluded_patterns = read_excluded_patterns_from_file(excluded_patterns_file)  # Load patterns from file

  try:
    response = requests.get(url, headers=random_headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")

    # Create the target folder with subdirectories if needed
    os.makedirs(target_folder, exist_ok=True)

    for image in images:
      image_url = image.get("src")
      if image_url and image_url.startswith("http"):
        skip_download = False
        for pattern in excluded_patterns:
          if image_url.startswith(pattern):
            skip_download = True
            break  # Exit the inner loop if a match is found

        if not skip_download:  # Download only if not excluded
          filename = os.path.basename(image_url)
          filepath = os.path.join(target_folder, filename)

          try:
            image_response = requests.get(image_url, headers=random_headers)
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

  # Define the excluded patterns file (modify the filename as needed)
  excluded_patterns_file = "excluded_patterns.txt"

  scrape_images(target_url, target_folder, excluded_patterns_file)
