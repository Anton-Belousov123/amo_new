import hashlib
import hmac
import json
from datetime import datetime
import requests


secret_channel_key = '546583c5d9718c566b4408babcebaec818efa14d'
channel_id = 'b0e8dd4d-959b-4e93-9eba-ac7341282f6b'
account_id = '3ffc2923-4767-42f6-aaf4-a83e8208e5a0'


body = {
    'account_id': account_id,
    'title': 'ChatIntegration',
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

host = 'https://amojo.amocrm.ru'
response = requests.post(host + f'/v2/origin/custom/{channel_id}/connect', headers=headers, data=request_body)
print(response.text)