from configparser import ConfigParser
import os


cp = ConfigParser()
dataset = cp.read(os.path.join(os.path.dirname(__file__), '../config.ini'))


if len(dataset) != 1:
    raise ValueError("Failed to open/find all files")

CACHE_DIR = './cache'
IMAGES_DIR = './images'

YA_DISK_URL=cp.get("ENV", "YA_DISK_URL")
YA_DISK_API_GET_INFO=cp.get("ENV", "YA_DISK_API_GET_INFO")
YA_DISK_API_GET_RESOURCES=cp.get("ENV", "YA_DISK_API_GET_RESOURCES")
YA_DISK_PUBLIC_KEY=cp.get("ENV", "YA_DISK_PUBLIC_KEY")