from time import time
import sys
from random import choice
from local_testing import *
from lib.constants import *

K = 5
consistency = LINEARIZABILITY
ports = [5000, 3000, 3030, 5050, 5051, 5055, 8000, 8080, 8081, 9000]

def test3():
    print('Deploying 10 servers.')
    for p in ports:
        deploy(p, K, consistency)
    print('Deployments OK')
    sleep(10)
    print_graph()
    start = time()
    with open('./transactions/requests.txt') as f:
        for line in f.readlines():
            if line.startswith('insert'):
                _, key, value = line.split(', ')
                insert(key, value, choice(ports))
            elif line.startswith('query'):
                _, key = line.split(', ')
                query(key, choice(ports))
    test_replicas()
    print(f'Requests took {time()-start} seconds')
    

def test12():    
    print('Deploying 10 servers.')
    for p in ports:
        deploy(p, K, consistency)
    print('Deployments OK')
    sleep(10)
    print_graph()

    with open('./transactions/insert.txt', 'r') as f:
        lines = f.readlines()
        start = time()
        for line in lines:
            _, key, value = line.split(', ')
            insert(key, value, choice(ports))
        end = time()
        print(f'Insertions took {end-start} seconds')

    with open('./transactions/query.txt', 'r') as f:
        lines = f.readlines()
        start = time()
        for line in lines:
            _, key = line.split(', ')
            query(key, choice(ports))
        end = time()
        print(f'Queries took {end-start} seconds')

if __name__ == '__main__':
    test12()
    # test3()