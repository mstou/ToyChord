#!/usr/bin/python3

import subprocess
import threading
import requests
import json
from time import sleep

PORTS = set()
K = 5

def debug(s):
    print('\033[96m' + s + '\033[0m')

def print_error(s):
    print(f'\u274c {s}')

def deploy(port):
    print(f'deploying server at port {port}')
    if port not in PORTS:
        PORTS.add(port)

    def aux(port):
        command = f'python3 node.py --port {port} -k {K} --local'.split(' ')
        if port == 5000:
            command.append('--bootstrap')
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    t = threading.Thread(target=aux, args=(port,))
    t.start()
    sleep(10)

def depart(port):
    print(f'Node at port {port} is departing', end=' ')
    response = requests.get(f'http://localhost:{port}/depart')
    if response.status_code == 200:
        PORTS.remove(port)
        print('OK')
    else:
        print('\033[91mFAILED\033[0m') # red color

    sleep(5)

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
        print_error('FAILED')

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
        print(f"node {node['me']['port']} files:")
        for key in node['files']:
            print(f"    {key} -> {node['files'][key]}")
    print('--------------------------------')

def print_graph():
    nodes = all_nodes()
    next = {str(node['me']['port']): node['next']['port'] for node in nodes}
    print('Network topology: ', end='')
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
    print('...\n')

def get_next_k(node, k, nodes):
    curr = node
    next_k = []
    for _ in range(k):
        curr = nodes[curr['next']['port']]
        next_k.append(curr)
    return next_k

def test_replicas():
    print('------Testing replicas-------')
    errors = False
    nodes = {str(port): log(port, False) for port in PORTS}
    for port, node in nodes.items():
        next_k = get_next_k(node, K-1, nodes)
        for key, file in node['files'].items():
            for i, replica_node in enumerate(next_k):
                if i >= len(replica_node['replicas']):
                    errors = True
                    print_error(f"Node {replica_node['me']['port']} does not have replicas at index {i}")
                elif key not in replica_node['replicas'][i]:
                    print_error(f"File with name {file['name']} and key {key} is not present in node {replica_node['me']['port']}")
                    errors = True
    if not errors:
        print('All replicas are in place' + ' \u2705')

def main():
    deploy(5000)
    deploy(4000)
    deploy(3000)
    deploy(5050)
    deploy(8080)
    # servers are deployed at this point
    print_graph()
    sleep(1)
    print('Inserting some keys targeting the nodes')
    for port in PORTS:
        insert(f'127.0.0.1:{port}', f'testing port {port}', port)
    print_all_files()
    test_replicas()
    print('Adding one more server')

    deploy(8000)
    sleep(10)
    insert('NikosKoukos', 'agorimou', 3000)
    insert('NikosKalantas', 'DiaThalasseos', 5000)
    test_replicas()
    delete('NikosKoukos', 5000)
    test_replicas()

    insert('deleteMe', 'now', 4000)
    delete('deleteMe', 3000)
    test_replicas()

    print_all_files()

    deploy(9000)
    sleep(10)
    test_replicas()

    files = ['asdlkjfpuo', 'alkjhw10912``asld', 'asdf123', '123adzxce', 'asldk']

    for s in files:
        insert(s, s + ' value', 3000)

    test_replicas()

    depart(8000)
    sleep(10)
    test_replicas()

if __name__ == '__main__':
    main()
    p = print_all_files # to use with python shell
    t = test_replicas
