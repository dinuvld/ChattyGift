import requests
import signature
import logging
import time

base_url = 'https://app.sandbox.reward.cloud/api/v2'
def issue_digital_card(brand, value):
    response = signature.generate_branded_request('POST', brand, value)
    return response.text

def get_brand_info():
    url = base_url + '/brands'
    headers = header.generate_branded_header('POST', 'nike', 12)
    response = requests.get(url, headers = headers)
    return response.content