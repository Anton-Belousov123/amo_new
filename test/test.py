import hashlib
import hmac
import json
from datetime import datetime
import requests


secret_channel_key = 'c506ff3d57fca1998e50ea8076ef7afc27934f65'
channel_id = '0de9c1dd-b5d8-4b38-bb7f-ef238bb3ca86'
account_id = '7eb31c63-e74d-41cd-86f7-34c6265386f9'
scope_id = 'scope_id'

body = {
    'account_id': account_id,
    'title': '',
    'hook_api_version': 'v2'
}
request_body = json.dumps(body)
checksum = hashlib.md5(request_body.encode('utf-8')).hexdigest()

now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')
data = request_body.encode('utf-8') + now.encode('utf-8')
signature = hmac.new(secret_channel_key.encode('utf-8'), json.dumps(body).encode('UTF-8'), hashlib.sha1).hexdigest()

headers = {
    'Date': now,
    'Content-Type': 'application/json',
    'Content-MD5': checksum.lower(),
    'X-Signature': signature.lower(),
}

response = requests.get(f'https://amojo.amocrm.ru/v2/origin/custom/{scope_id}/chats/9389b299-c47b-4607-aad1-3a7baa307bbd/history',
                        headers=headers, data=request_body)
print(response.status_code)
print(response.text)