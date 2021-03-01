import requests
from time import sleep
from lib.constants import *

def join_request(targetNode, port, ip):
    sleep(5)
    url = HTTP + targetNode.get_address() + '/join'
    params = f'{PORT}={port}&{IP}={ip}'
    requests.get(url + '?' + params)

def update_previous_request(targetNode, port, ip, cur_previous):
    url = HTTP + targetNode.get_address() + '/update_previous'
    params = f'{PORT}={port}&{IP}={ip}&{CUR_PREVIOUS}={cur_previous}'
    requests.get(url + '?' + params)

def join_successful_request(target, previous, next):
    url = HTTP + target.get_address() + '/join_successful'
    params = f'{NEXT_PORT}={next.get_port()}&{NEXT_IP}={next.get_ip()}' +\
             f'{PREV_PORT}={previous.get_port()}&{PREV_IP}={previous.get_ip()}'
    requests.get(url + '?' + params)
