import requests
import time as t
url = 'https://www.reddit.com/r/todayilearned/new/.json'


class VariableThings:
    previous_title = ''
    newPost = True


fr = open('TIL facts.txt', 'r')
lines = []
for i in enumerate(fr):
    lines.append(i)
fr.close()
numberOfLines = len(lines)
lastTitleLine = numberOfLines - 5
VariableThings.previous_title = lines[lastTitleLine][1][:-1]


def get_new_post():
    raw_data = requests.get(url, headers={'User-agent': 'Parth bot 0.002'})
    json_data = raw_data.json()
    raw_title = json_data['data']['children'][0]['data']['title']
    other_data = json_data['data']['children'][0]['data']
    clean_title(raw_title, other_data)


def clean_title(text, data):
    clean_text = text[4:]
    if 'that' in clean_text[:6]:
        clean_text = clean_text[5:]
    clean_text = clean_text[:1].upper() + clean_text[1:]
    check_fact(clean_text, VariableThings.previous_title, data)
    VariableThings.previous_title = clean_text


def check_fact(new, old, data):
    if new == old:
        if VariableThings.newPost:
            print('No new fact available.')
        VariableThings.newPost = False
        return
    else:
        useful_data = {'title': new, 'upvotes': str(data['ups']), 'downvotes': str(data['downs']),
                       'post_time': data["created_utc"], 'permalink': data['permalink'], 'author': data['author'],
                       'link': data['url']}
        print_fact(useful_data)
        VariableThings.newPost = True


def print_fact(data):
    text_data = {'fact':
                 data['title'] + '\nLink: ' + data['link'] + '\nPermalink: ' + 'www.reddit.com' + data['permalink'] +
                 '\nSubmitter: ' + data['author'] + '\tDate posted: ' + t.asctime(t.localtime(data['post_time'])) +
                 '\n\n'
                 }

    fw = open('TIL Facts.txt', 'a')
    fw.write(text_data['fact'])
    fw.close()
    print(text_data['fact'])


while True:
    get_new_post()
    t.sleep(30)


