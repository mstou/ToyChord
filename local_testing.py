#!/usr/bin/python3

import subprocess
import threading
import requests
import json
from time import sleep

def deploy(port, bootstrap=False):
    if bootstrap:
        subprocess.run(['python3', 'node.py', str(port), 'bootstrap'])
    else:
        subprocess.run(['python3', 'node.py', str(port)])

def pretty(response):
    return json.dumps(response.json(), indent=4, sort_keys=True)

def log(port, verbose=False):
    url = f'http://localhost:{port}/log'
    if verbose:
        print(f'-----------{url}------------------')
    response = requests.get(url)
    if verbose:
        print(pretty(response))
    return response.json()

def insert(key, value, port):
    print(f'inserting {key} -> {value}...', end=' ')
    response = requests.get(f'http://localhost:{port}/insert?key={key}&value={value}')
    if response.status_code == 200:
        print('OK')
    else:
        print('\033[91mFAILED\033[0m') # red color

def main():
    t5000 = threading.Thread(target=deploy, args=(5000, 'bootstrap'))
    t3000 = threading.Thread(target=deploy, args=(3000,))
    t4000 = threading.Thread(target=deploy, args=(4000,))
    
    server_threads = [t5000, t4000, t3000]
    for server_thread in server_threads:
        server_thread.start()
        sleep(5)
    
    # servers are deployed at this point

    node5000 = log(5000, verbose=True)
    node4000 = log(4000, verbose=True)
    node3000 = log(3000, verbose=True)
    nodes = [node5000, node4000, node3000]
    print('---------------------------------------------------')
    for node in nodes:
        print(f"{node['previous']['port']} <- {node['me']['port']} -> {node['next']['port']}")
    print('---------------------------------------------------')
    sleep(1)
    insert('key1', 'NikosKoukos', 5000)
    insert('key2', 'NikosKalantas', 3000)
    insert('key3', 'NikosKorompos', 4000)
    
    nodes = [log(5000), log(4000), log(3000)]
    for node in nodes:
        print('-----------------------')
        print(f"node {node['me']['port']} files:")
        print(node['files'])
    
if __name__ == '__main__':
    main()