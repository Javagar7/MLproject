import argparse
import json
import itertools
import logging
import re
import os
import uuid
import sys
from urllib.request import urlopen, Request
from urllib.parse import parse_qs, urljoin # Add this line
from urllib.parse import parse_qs
from bs4 import BeautifulSoup


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    Filehandler = logging.FileHandler("./log.txt") #Path to your LOG FILE.
    Filehandler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(Filehandler)
    
    return logger

logger = configure_logging()

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    # 'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
    }


def get_soup(url, header):
    try:
        response = urlopen(Request(url, headers=header))
        return BeautifulSoup(response, 'html.parser')
    except:
        return None


def get_query_url(query):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query

def findImageUrl(url):
    res = parse_qs(url)    
    if 'url' in res:
        return res['url'][0]
    else:
        return None

def extract_images_from_soup(soup, base_url):
    link_elements = soup.find_all("a")
    links = [findImageUrl(e.get('href')) for e in link_elements]
    image_page_links = list(filter(lambda l: l != None, links))

    all_image_links = []

    for page_url in image_page_links:
        soup_page = get_soup(page_url, REQUEST_HEADER)
        if soup_page:
            for img_el in soup_page.find_all("img"):
                if img_el:
                    h = img_el.get('height')
                    w = img_el.get('width')

                    try:
                        if h and w and float(h) >= 640 and float(w) >= 640:  # Minimum image size check
                            if "http" in img_el.get('src') or "https" in img_el.get('src'):
                                all_image_links.append(img_el.get('src'))
                            elif "data" not in img_el.get('src'):
                                absolute_image_url = urllib.parse.urljoin(base_url, img_el.get('src'))
                                all_image_links.append(absolute_image_url)
                            # print(all_image_links)
                    except:
                        pass

    return all_image_links



def extract_images(query, num_images):
    url = get_query_url(query)
    logger.info("Souping")
    soup = get_soup(url, REQUEST_HEADER)
    logger.info("Extracting image urls")
    link_type_records = extract_images_from_soup(soup, url)
    return itertools.islice(link_type_records, int(num_images))

def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'
    file_name = uuid.uuid4().hex + "." + extension
    save_path = os.path.join(save_directory, file_name)

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)


def download_images_to_dir(images, save_directory, num_images):
    for i, url in enumerate(images):
        if url and '.jpg' in url:
            try:
                logger.info("Making request (%d/%d): %s", i, num_images, url)
                raw_image = get_raw_image(url)
                save_image(raw_image, 'jpg', save_directory)
            except Exception as e:
                logger.exception(e)

def run(query, save_directory, num_images=100):
    print(save_directory)
    query = '+'.join(query.split())
    print(query)
    logger.info("Extracting image links")
    images = extract_images(query, num_images)
    logger.info("Downloading images")
    download_images_to_dir(images, save_directory, num_images)
    logger.info("Finished")

def main():
    # parser = argparse.ArgumentParser(description='Scrape Google images')

    # if not os.path.isdir('./download'):
    #     os.mkdir('./download')

    # parser.add_argument('-s', '--search', required=True, type=str, help='search term')
    # parser.add_argument('-n', '--num_images', default=100, type=int, help='num images to save')
    # parser.add_argument('-d', '--directory', default='./download', type=str, help='save directory')
    # args = parser.parse_args()

    # if not os.path.isdir(args.directory):
    #     os.mkdir(args.directory)
    search = input("image need: ")
    directory = input("where to store: ")
    num_images = input("how many: ")

    run(search, directory, num_images)

if __name__ == '__main__':
    main()

