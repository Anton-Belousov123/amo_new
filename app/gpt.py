import json
import os

import openai

from app import sheets, deepl
import dotenv

dotenv.load_dotenv('misc/.env')


def what_is_the_question(question, m):
    task = [{'role': 'system',
             'content': 'Write only digit. (0 or 1 or 2 or 3 or 4 or 5 or 6). Your task is to classificate question in array of possible questions.'
                        f' Возможные варианты: 0 - {m[0]};'
                        f'1 - {m[1]};'
                        f'2 - {m[2]};'
                        f'3 - {m[3]};'
                        f'4 - {m[4]};'
                        f'5 - {m[5]};'
                        f'6 - {m[6]};'
             }]
    task.append({'role': 'user', 'content': "Question: " + question})
    answer = get_answer(task, 3)
    while '0' not in answer and '1' not in answer and '2' not in answer and '3' not in answer \
            and '4' not in answer and '5' not in answer and '6' not in answer:
        answer = get_answer(task, 3)
    for i in range(7):
        if str(i) in answer:
            return i


def is_answer_correct(question, answer):
    task = [{'role': 'system',
             'content': 'Write only digit (0 or 1). You have Q&A. You task is to check, is answer is possible for this question (1) or not (0). In question you should consider only the interrogative sentence.'
             }]
    task.append({'role': 'assistant', 'content': "Question: " + question})
    task.append({'role': 'user', 'content': "Answer: " + answer})
    answer = get_answer(task, 3)
    while '1' not in answer and '0' not in answer:
        answer = get_answer(task, 3)
    if '1' in answer:
        return 1
    return 0


def prepare_request(amo_messages):
    messages = []
    print('Вопрос:', amo_messages[1]['text'])
    print('Ответ:', amo_messages[0]['text'])
    rules, length, messages = sheets.read_message_preview()
    text_length = len(rules)
    if amo_messages[0]['text'] != '/restart':
        index = what_is_the_question(amo_messages[1]['text'], messages)
        status = True
        if index != 0:
            status = is_answer_correct(amo_messages[1]['text'], amo_messages[0]['text'])
        print('Ответ корректен:', bool(status))

        if status == 0 or index + 1 >= len(messages):
            messages.append({'role': 'system', 'content': messages[index]})
        else:
            messages.append({'role': 'system', 'content': messages[index + 1]})
        print('Следующий вопрос:', messages[-1]['content'])

    for amo_message in amo_messages:
        if text_length + len(amo_message['text']) > 4000:
            break
        text_length += len(amo_message['text'])
        if amo_message['author']['id'] == '6bbb0237-32bc-4b1f-bcd5-411574e8912c':
            messages.append({"role": "assistant", "content": amo_message['text']})
        else:
            messages.append({"role": "user", "content": amo_message['text']})
    messages.append({'role': 'system', 'content': rules})

    response = []
    for i in messages:
        try:
            if i['content'] == '/restart':
                break
            response.append(i)
        except:
            pass
    if len(response) == 0:
        response.append({"role": "user", "content": "Привет. Я новый клиент."})
        response.append({'role': 'system', 'content': rules})
        response.append({'role': 'system', 'content': messages[0]})
    response.reverse()
    return response, length


def get_answer(messages: list, limit):
    l, t = deepl.translate_it(str(messages), 'EN')
    messages = json.loads(t.replace("'", '"'))
    try:
        # if True:
        openai.api_key = os.getenv('CHAT_GPT_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=int(limit)
        )
        if response['choices'][0]['message']['content'].count('?') > 1:
            return get_answer(messages, limit)

        return deepl.translate_it(response['choices'][0]['message']['content'], l)

    except Exception as e:
        print('Ошибка', e)
        return get_answer(messages, limit)
