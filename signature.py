import time
import hmac
import hashlib
import requests
import json

api_key = '5e9089d4fc44c3c357b4d46b91a52b440ac6acf7b5680caebb695994ad27750c'
secret_key = bytearray('3e76857dd94e6d07eddd946a11f2211874bf7e89c85b49e8b4a3c3afdee5fbbe', 'utf-8')
endpoint = 'digital-issue'
client_request_id = int(time.time() - 1)

def generate_timestamp():
    return str(int(round(time.time() * 1000)))

def generate_signature_seed(request_type, brand, face_value, timestamp):
    face_value = str(face_value)
    return api_key + '-' + request_type + '-' + endpoint + '-' + str(client_request_id) + '-' + brand + '-' + 'GBP' + '-' + face_value + '-' + timestamp

def generate_signature(request_type, brand, face_value, timestamp):
    seed = generate_signature_seed(request_type, brand, face_value, timestamp)
    signature_hmac = hmac.new(secret_key, bytearray(seed, 'utf-8'), hashlib.sha256)
    signature = str(signature_hmac.hexdigest())
    print(seed)
    print()
    print(signature)
    return signature

api_key = '5e9089d4fc44c3c357b4d46b91a52b440ac6acf7b5680caebb695994ad27750c'
boilerplate_header = {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json',
    'API-Key': api_key,
    'Signature': None,
    'Timestamp': None,
}

def generate_branded_request(request_type, brand, face_value):
    payload = {
        'client_request_id': str(client_request_id),
        'brand': brand,
        'face_value': {
            'amount': face_value,
            'currency': 'GBP'
        },
        'delivery_method': 'code',
        'fulfilment_by': 'rewardcloud',
        'fulfilment_parameters': {
            'to_name': 'Vlad',
            'to_email': 'vlad@hotmail.com',
            'from_name': 'Reward Cloud',
            'from_email': 'noreply@reward.cloud',
            'subject': '[TestCode] Here is your gift card!'
        },
        'personalisation': {
            'to_name': 'Recipient',
            'from_name': 'Sender',
            'message': 'Here is your gift',
            'template': 'standard'
        },
        'sector': 'voluntary-benefits'
    }
    header = boilerplate_header
    timestamp = str(int(time.time()*1000))
    header['Signature'] = generate_signature(request_type, brand, face_value, timestamp)
    header['Timestamp'] = timestamp
    url = 'https://app.sandbox.reward.cloud/api/v2/digital/issue'
    response = requests.request(request_type, url, headers=header, data = json.dumps(payload))
    return response


