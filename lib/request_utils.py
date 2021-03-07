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

def insert_replica_request(targetNode, key, value, number):
    url = HTTP + targetNode.get_address() + '/insert_replica'
    params = f'{KEY}={key}&{VALUE}={value}&{NUMBER}={number}'
    requests.get(url + '?' + params)

def increase_replicas_in_range_request(targetNode, number):
    url = HTTP + targetNode.get_address() + '/increase_replicas_in_range'
    params = f'{NUMBER}={number}'
    requests.get(url + '?' + params)

def increase_replica_request(targetNode, key):
    url = HTTP + targetNode.get_address() + '/increase_replica'
    params = f'{KEY}={key}'
    requests.get(url + '?' + params)

def delete_request(targetNode, key):
    url = HTTP + targetNode.get_address() + '/delete'
    params = f'{KEY}={key}'
    requests.get(url + '?' + params)

def delete_replica_request(targetNode, key, number):
    url = HTTP + targetNode.get_address() + '/delete_replica'
    params = f'{KEY}={key}&{NUMBER}={number}'
    requests.get(url + '?' + params)

def query_request(targetNode, key):
    url = HTTP + targetNode.get_address() + '/query'
    params = f'{KEY}={key}'
    result = requests.get(url + '?' + params)
    return result

def update_next_request(targetNode, port, ip, cur_next):
    url = HTTP + targetNode.get_address() + '/update_next'
    params = f'{PORT}={port}&{IP}={ip}&{CUR_NEXT}={cur_next}'
    requests.get(url + '?' + params)

def get_all_files_request(targetNode):
    url = HTTP + targetNode.get_address() + '/get_all_files'
    result = requests.get(url)
    return result

def update_prev_request(targetNode, port, ip, cur_prev):
    url = HTTP + targetNode.get_address() + '/update_prev'
    params = {
        PORT: port,
        IP: ip,
        CUR_PREV: cur_prev,
    }
    requests.get(url, params=params)

def join_successful_request(target, previous, next):
    url = HTTP + target.get_address() + '/join_successful'
    params = f'{NEXT_PORT}={next.get_port()}&{NEXT_IP}={next.get_ip()}' +\
             f'&{PREV_PORT}={previous.get_port()}&{PREV_IP}={previous.get_ip()}'
    print(f'Requesting page {url + "?" + params}')
    requests.get(url + '?' + params)
