import requests
from time import sleep
from lib.constants import *

def join_request(targetNode, port, ip):
    sleep(2)
    url = HTTP + targetNode.get_address() + '/join'
    params = f'{PORT}={port}&{IP}={ip}'
    requests.get(url + '?' + params)

def insert_request(targetNode, key, value):
    url = HTTP + targetNode.get_address() + '/insert'
    params = f'{KEY}={key}&{VALUE}={value}'
    requests.get(url + '?' + params)

def delete_request(targetNode, key):
    url = HTTP + targetNode.get_address() + '/delete'
    params = f'{KEY}={key}'
    requests.get(url + '?' + params)

def update_next_request(targetNode, port, ip, cur_next):
    url = HTTP + targetNode.get_address() + '/update_next'
    params = f'{PORT}={port}&{IP}={ip}&{CUR_NEXT}={cur_next}'
    requests.get(url + '?' + params)

def join_successful_request(target, previous, next):
    url = HTTP + target.get_address() + '/join_successful'
    params = f'{NEXT_PORT}={next.get_port()}&{NEXT_IP}={next.get_ip()}' +\
             f'&{PREV_PORT}={previous.get_port()}&{PREV_IP}={previous.get_ip()}'
    print(f'Requesting page {url + "?" + params}')
    requests.get(url + '?' + params)
