import os
import zipfile
import requests
from config import YA_DISK_URL, YA_DISK_API_GET_INFO, YA_DISK_API_GET_RESOURCES, YA_DISK_PUBLIC_KEY, CACHE_DIR, IMAGES_DIR

def get_info() -> list:
  try:
    response = requests.get(
      YA_DISK_URL + YA_DISK_API_GET_INFO,
      headers={
        "Accept": "application/json",
      }, params={
        "public_key": YA_DISK_PUBLIC_KEY,
      })
    info = response.json()['_embedded']['items']
    return info

  except Exception as e:
    print(f"Error: {e}")
    return []
  
def get_resources(path) -> None:
  try:
    response = requests.get(
      YA_DISK_URL + YA_DISK_API_GET_RESOURCES,
      headers={
        "Accept": "application/json",
      }, params={
        "public_key": YA_DISK_PUBLIC_KEY,
        "path": path
      })
    
    data = response.json()

    download_link = data['href']
    download_method = data['method']

    response = requests.request(download_method, download_link)

    print('Downloading folder: ' + path)
    with open(os.path.join(CACHE_DIR, 'file.zip'), 'wb') as f:
      f.write(response.content)
    print('Folder downloaded successfully')

    # Unzip the downloaded file
    with zipfile.ZipFile(os.path.join(CACHE_DIR, 'file.zip'), 'r') as zip_ref:
      zip_ref.extractall(IMAGES_DIR)
    print('Folder unzipped successfully')
  except Exception as e:
    print(f"Error: {e}")