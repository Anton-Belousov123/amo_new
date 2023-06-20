import requests
import hashlib
import hmac
import datetime


# Constants
secret = '546583c5d9718c566b4408babcebaec818efa14d'
conversation_id = '0a0cd598-3b2c-4e0c-8872-413844567e0a'
scope_id = 'b0e8dd4d-959b-4e93-9eba-ac7341282f6b_3ffc2923-4767-42f6-aaf4-a83e8208e5a0'

# Usable variables
date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
content_type = 'application/json'
path = f'/v2/origin/custom/{scope_id}/chats/{conversation_id}/history'
url = f'https://amojo.amocrm.ru' + path


# Main login
check_sum = hashlib.md5(b'').hexdigest()
message = '\n'.join(["GET", check_sum, content_type, date, path]).encode('utf-8')
signature = hmac.new(secret.encode('utf-8'), message, hashlib.sha1).hexdigest()


# Request
headers = {
    'Date': date,
    'Content-Type': content_type,
    'Content-MD5': check_sum,
    'X-Signature': signature,
}
response = requests.get(url=url, headers=headers)

print(f"Status: {response.status_code}")
print(response.text)