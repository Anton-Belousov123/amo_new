import time

import requests


def get_token():
    try:
        session = requests.Session()
        response = session.get('https://kevgenev8.amocrm.ru/')
        session_id = response.cookies.get('session_id')
        csrf_token = response.cookies.get('csrf_token')
        headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': f'session_id={session_id}; '
                      f'csrf_token={csrf_token};'
                      f'last_login=kevgenev8@mail.ru',
            'Host': 'kevgenev8.amocrm.ru',
            'Origin': 'https://kevgenev8.amocrm.ru',
            'Referer': 'https://kevgenev8.amocrm.ru/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        payload = {
            'csrf_token': csrf_token,
            'password': "Xh1wdBlk",
            'temporary_auth': "N",
            'username': "kevgenev8@mail.ru"}

        response = session.post('https://kevgenev8.amocrm.ru/oauth2/authorize', headers=headers, data=payload)
        access_token = response.cookies.get('access_token')
        refresh_token = response.cookies.get('refresh_token')
        headers['access_token'] = access_token
        headers['refresh_token'] = refresh_token
        payload = {
            'request[chats][session][action]': 'create'
        }
        response = session.post('https://kevgenev8.amocrm.ru/ajax/v1/chats/session', headers=headers, data=payload)
        token = response.json()['response']['chats']['session']['access_token']
    except:
        time.sleep(3)
        return get_token()
    print('New token:', token)
    return token, session


