import argparse
import os
import time
from io import BytesIO

from PIL import Image
import requests

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--category', default='real',
    help = 'category of image',
    choices=['real', 'ai'])
parser.add_argument('--keyword', type=str,
                    help = 'name of your image content')
parser.add_argument('--limit', default=20, type=int,
    help = 'number of returned results')

args = parser.parse_args()
options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
# driver = webdriver.Edge()

def scrape_image(category, keyword, limit, output_dir):
    if category == 'ai':
        driver.get("https://www.freepik.com/search?format=search&last_filter=type&last_value=ai&query={}&type=ai".format(keyword))
    else:
        driver.get("https://www.freepik.com/search?format=search&query=real%20{}&type=photo".format(keyword))

# time.sleep(5)
    for i in range(1, limit+1):
        img_link = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/section/figure[{}]/div/a/img".format(i))
        src = img_link.get_attribute('src')

        # Download the image using requests
        response = requests.get(src)
        if response.status_code == 200:
            # Create a PIL image object from the downloaded image data
            image = Image.open(BytesIO(response.content))

            # Resize the image to 300x300 pixels
            resized_image = image.resize((300, 300))

            # Save the resized image
            resized_image.save(output_dir+"/image_{}.png".format(i))

if args.keyword is not None:
    print(args.keyword)
    output_dir = '{}_images/{}'.format(args.category, args.keyword)
    os.makedirs(output_dir, exist_ok=True)
    scrape_image(args.category, args.keyword, args.limit, output_dir)

else:
    print('Default scrape data topic as coco dataset')
    with open('coco.names', "r") as f:
        names = f.read().splitlines()
    for key in names:
        print(key)
        output_dir = '{}_images/{}'.format(args.category, key)
        os.makedirs(output_dir, exist_ok=True)
        scrape_image(args.category, key, args.limit, output_dir)

print(driver.title)