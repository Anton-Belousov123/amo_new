import asyncio
import json
import os
import time

import bs4
from flask import Flask, request
import requests
import dotenv
from app import gpt, auth
from app.gpt import get_answer


def get_pipeline(image, s_name, text):
    from app.auth import get_token
    token, session = get_token()
    url = 'https://kevgenev8.amocrm.ru/leads/pipeline/6731170/?skip_filter=Y'

    response = session.get(url, timeout=15)
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    for i in soup.find_all('div', {'class': 'pipeline-unsorted__item-data'}):
        img = i.find('div', {'class': 'pipeline-unsorted__item-avatar'}). \
            get('style').replace("background-image: url(", '').replace(')', '')

        name = i.find('a', {'class': 'pipeline-unsorted__item-title'}).text
        message = i.find('div', {'class': 'pipeline_leads__linked-entities_last-message__text'}).text
        pipeline = i.find('a', {'class': 'pipeline-unsorted__item-title'}).get('href').split('/')[-1]
        if (img == image) or (message == text and s_name == name):
            return pipeline
    return None

dotenv.load_dotenv('misc/.env')

token = ''
app = Flask(__name__)
account_chat_id = os.getenv('ACCOUNT_CHAT_ID')
print(account_chat_id)
user_dict = {}


def send_message(receiver_id: str, message: str):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'
    response = requests.post(url, headers=headers, data=json.dumps({"text": message}))


def get_chat_history(receiver_id: str):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/messages/{account_chat_id}/merge?stand=v15' \
          f'&offset=0&limit=100&chat_id%5B%5D={receiver_id}&get_tags=true&lang=ru'
    message_list = requests.get(url, headers=headers).json()
    return message_list['message_list']


def get_id(headers):
    url = 'https://kevgenev8.amocrm.ru/leads/pipeline/6731170/?skip_filter=Y'
    response = requests.get(url, headers=headers)


@app.route('/webapp', methods=["POST"])
def webapp():
    global token
    d = request.form.to_dict()
    if int(d['message[add][0][created_at]']) + 10 < int(time.time()):
        return 'ok'
    receiver_id = d['message[add][0][chat_id]']
    print(receiver_id, 'rec-id')


def send_notes(pipeline_id, session, text):
    url = f'https://kevgenev8.amocrm.ru/private/notes/edit2.php?parent_element_id={pipeline_id}&parent_element_type=2'
    data = {
        'DATE_CREATE': int(time.time()),
        'ACTION': 'ADD_NOTE',
        'BODY': text,
        'ELEMENT_ID': pipeline_id,
        'ELEMENT_TYPE': '2'
    }
    resp = session.post(url, data=data)
    print(resp.text)


def translate_it(m):
    messages = [
        {'role': 'system', 'content': f"Translate this text to Russian: {m}"}
    ]
    return get_answer(messages, 4000)


@app.route('/', methods=["POST"])
def hello():
    global token
    d = request.form.to_dict()
    print(d)
    if 'message[add][0][author][avatar_url]' not in d:
        image = ''
    else:
        image = d['message[add][0][author][avatar_url]']
    name = d['message[add][0][author][name]']
    text = d['message[add][0][text]']
    pipeline = get_pipeline(image, name, text)
    if pipeline is None:
        print('Not this thread!')
        return
    if int(d['message[add][0][created_at]']) + 10 < int(time.time()):
        return 'ok'
    receiver_id = d['message[add][0][chat_id]']
    if d['message[add][0][text]'] == 'Зарегистрироваться в WebApp':
        return 'ok'

    while True:
        try:
            chat_history = get_chat_history(receiver_id)
        except Exception as e:
            print(e, 1)
            token, session = auth.get_token()
            continue
        break
    fl = False
    alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё',
                'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
                'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    for s in d['message[add][0][text]']:
        if s in alphabet: fl = True
    if not fl:
        pipeline = get_pipeline(image, name, text)
        translation = translate_it(text)
        token, session = auth.get_token()
        send_notes(pipeline, session, translation)
    prepared_request, limit = gpt.prepare_request(chat_history)
    message = gpt.get_answer(prepared_request, limit)
    while True:
        try:
            send_message(receiver_id, message)
        except Exception as e:
            print(e, 2)
            token, session = auth.get_token()
            continue
        break

    #    get_id(headers)

    fl = False
    for s in message:
        if s in alphabet: fl = True
    if not fl:
        pipeline = get_pipeline(image, name, text)
        translation = translate_it(message)
        token, session = auth.get_token()
        send_notes(pipeline, session, translation)

    return 'ok'


app.run(host='0.0.0.0', debug=True, port=8000)
