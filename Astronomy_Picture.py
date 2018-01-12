import datetime
import requests
import re
import io
from PIL import Image
from bs4 import BeautifulSoup

astro_date = ''
astro_URL = 'https://apod.nasa.gov/apod/ap%%.html'
astro_image_URL = 'https://apod.nasa.gov/apod/'
save_path = r"C:\Users\parth\Pictures\APOD"


def get_date():
    global astro_date
    try:
        date = input('Enter Date for the Astronomy picture you want to see. [dd/mm/yy] \n').split('/')
        date = list(map(int, date))
        x = str(datetime.datetime(year=date[2], month=date[1], day=date[0])).split('-')
        y1 = [x[0][2:], x[1], x[2][:2]]
        astro_date = ''.join(y1)
        return datetime.datetime(date[2], date[1], date[0])

    except ValueError or IndexError:
        print('Enter a valid date.')
        get_date()


def get_explanation():
    raw = soup.findAll('p')[2]
    pos = [m.start() for m in re.finditer('<p>', str(raw))]
    raw = str(raw)[:pos[1]]
    soup_ = BeautifulSoup(raw, 'html.parser')
    raw = str(soup_.findAll('p')[0].text)
    return (raw.replace('\n', ' ')).replace('  ', ' ')


def get_image():
    p = image_date.ctime()
    print("Astronomy Picture of the Day for " + p[4:-13] + "'" + p[-2:] + " is titled:")
    print(title)

    picture_path = soup.findAll('a')[1]
    image_link_full_res = astro_image_URL + picture_path.get('href')
    picture_path = soup.findAll('img')[0]
    image_link_compressed = astro_image_URL + picture_path.get('src')
    return {'compressed': image_link_compressed, 'full-res': image_link_full_res}


def display_image():
    picture_bytes = requests.get(image_links['compressed'])
    img_bytes = io.BytesIO(picture_bytes.content)
    image = Image.open(img_bytes)
    image.show()


def download_image():
    image_raw = requests.get(image_links['full-res'])
    image_bytes = io.BytesIO(image_raw.content)
    image = Image.open(image_bytes).convert("RGB")
    image.save(save_path + '\\' + title.replace(':', '') + '.jpg', format=None)


image_date = get_date()
image_URL = astro_URL.replace('%%', astro_date)
response = requests.get(image_URL)
if response.status_code != 200:
    print('The date entered is out of range. Please enter a date between January 1, 1995 and today.')
    exit('Invalid Date')
soup = BeautifulSoup(response.text, 'html.parser')

title = soup.findAll('b')[0].text

image_links = get_image()
image_explanation = get_explanation()

print(image_explanation)

y = input("Do you want to see the picture?")
if y.lower() in ['', 'y', 'yes']:
    display_image()

y = input("Do you want to download the Image?")
if y.lower() in ['', 'y', 'yes']:
    download_image()
