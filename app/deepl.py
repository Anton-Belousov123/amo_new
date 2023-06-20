import requests

headers = {
    'Host': 'api.deepl.com',
    'Authorization': 'DeepL-Auth-Key cd0d21a0-08bc-a2cd-992f-a2430aee94ce',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def translate_it(text: str, lang: str):
    response = requests.post('https://www.deepl.com/v2/translate', headers=headers, data={'text': text,
                                                                                          'target_lang': lang}).json()
    return response['translations'][0]['detected_source_language'], response['translations'][0]['text']

