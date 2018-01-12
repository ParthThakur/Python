from selenium import webdriver
from bs4 import BeautifulSoup


url = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
id_Table = 'mw-content-text'
PhantomJS_Path = r'C:\Users\parth\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\webdriver\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe'


def get_headers(r):
    soup = BeautifulSoup(r, 'html.parser')
    headers = soup.find_all('th')
    headers = BeautifulSoup(str(headers), 'html.parser').text.split(',')
    return clean(headers)


def clean(text):
    clean_headers = []
    for t in text:
        if t.find('[') == 0 or t.find(' ') == 0:
            t = t[1:]
        if 'A ' in t[:3]:
            t = t[2:]
        if '[' in t:
            p = t.find('[')
            clean_headers.append(t[:p])
        else:
            clean_headers.append(t)
    clean_headers = {'name_of_country': clean_headers[0],
                     'UN_member': clean_headers[1],
                     'sovereign_dispute': clean_headers[2],
                     'more_info': clean_headers[3]}
    return clean_headers


def get_data(d):
    while len(d) < 4:
        d.append('-')
    new_row = clean(d)
    print_row(new_row)


def print_row(d):
    print('{:60}{:35}{:20}{}'.format(d['name_of_country'], d['UN_member'], d['sovereign_dispute'], d['more_info']))


driver = webdriver.PhantomJS(PhantomJS_Path)
driver.get(url)
status = driver.find_element_by_id(id_Table)
raw = status.get_attribute('outerHTML')


# with open('wiki.txt', 'r', encoding='utf-8') as fr:
#     raw = fr.read()


soup = BeautifulSoup(raw, 'html.parser')
raw = soup.find_all('table')
raw = BeautifulSoup(str(raw[0]), 'html.parser').find_all('tr')
raw_data = []
data = []
for x in raw:
    raw_data.append(str(x))
top_row = get_headers(raw_data[0])
print_row(top_row)
count = 0

for x in raw_data:
    s = BeautifulSoup(x, 'html.parser')
    s = s.find_all('tr')
    if 'class="flagicon"' in str(s):
        data.append(str(s))


for new_rows in data:
    row = BeautifulSoup(new_rows[1:-1], 'html.parser')
    row_text = list(filter(None, row.text.split('\n')))
    get_data(row_text)
    # if count > 20:
    #     exit()
    # count += 1
