#!/usr/bin/python3

import subprocess
import threading
import requests
import json
from time import sleep

PORTS = set()

def deploy(port):
    if port not in PORTS:
        PORTS.add(port)
    def aux(port):
        if port == 5000:
            subprocess.run(['python3', 'node.py', str(port), 'bootstrap'])
        else:
            subprocess.run(['python3', 'node.py', str(port)])
    t = threading.Thread(target=aux, args=(port,))
    t.start()
    sleep(5)

def depart(port):
    print(f'Node at port {port} is departing', end=' ')
    response = requests.get(f'http://localhost:{port}/depart')
    if response.status_code == 200:
        PORTS.remove(port)
        print('OK')
    else:
        print('\033[91mFAILED\033[0m') # red color

def pretty(response):
    return json.dumps(response.json(), indent=4, sort_keys=True)

def log(port, verbose=True):
    url = f'http://localhost:{port}/log'
    if verbose:
        print(f'-----------{url}------------------')
    response = requests.get(url)
    if verbose:
        print(pretty(response))
    return response.json()

def insert(key, value, port):
    print(f'inserting at node {port}: {key} -> {value}...', end=' ')
    response = requests.get(f'http://localhost:{port}/insert?key={key}&value={value}')
    if response.status_code == 200:
        print('OK')
    else:
        print('\033[91mFAILED\033[0m') # red color

def delete(key, port):
    print(f'deleting key {key} from port {port}...', end=' ')
    response = requests.get(f'http://localhost:{port}/delete?key={key}')
    if response.status_code == 200:
        print('OK')
    else:
        print('\033[91mFAILED\033[0m') # red color

def query(key, port=5000, verbose=True):
    url = f'http://localhost:{port}/query'
    params = {
        'key': key
    }
    if verbose:
        print(f'----Query key={key}, url={url}----')
    response = requests.get(url, params=params)
    if verbose:
        print(pretty(response))
    return response.json()

def all_nodes():
    return [log(port, False) for port in PORTS]

def print_all_files():
    nodes = all_nodes()
    for node in nodes:
        print('-----------------------')
        print(f"node {node['me']['port']} files:")
        for key in node['files']:
            print(f"{key} -> {node['files'][key]}")
    print('--------------------------------')

def print_graph():
    nodes = all_nodes()
    next = {node['me']['port']: node['next']['port'] for node in nodes}
    print('---------------------------------------------------')
    frontier = ['5000']
    visited = set()
    while frontier:
        node = frontier[0]
        visited.add(node)
        print(f"{node} -> ", end='')
        if next[node] not in visited:
            frontier = [next[node]]
        else:
            frontier = []
    print('...\n---------------------------------------------------')

def main():
    deploy(5000)
    deploy(4000)
    deploy(3000)
    # servers are deployed at this point

    print_graph()
    
    sleep(1)

    for port in PORTS:
        insert(f'127.0.0.1:{port}', f'testing port {port}', port)
    
    print_all_files()

if __name__ == '__main__':
    main()
    p = print_all_files # to use with python shell