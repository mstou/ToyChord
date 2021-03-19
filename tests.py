import sys
import argparse
from time import time
from random import choice
from local_testing import *
from lib.constants import *

parser = argparse.ArgumentParser()
parser.add_argument("-k", type=int)
parser.add_argument("--eventual", action="store_true")
args = parser.parse_args()

K = 3 if args.k == None else args.k
consistency = EVENTUAL if args.eventual else LINEARIZABILITY

ports = [5000, 3000, 3030, 5050, 5051, 5055, 8000, 8080, 8081, 9000]

output_file = open(f'{K}_{consistency}_{time()}', 'w')

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
    operations_time = time()-start
    print(f'Requests took {operations_time} seconds')

    print(f'{operations_time}', file = output_file)

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
            key, value = line.split(', ')
            insert(key, value, choice(ports))
        end = time()
        insertions_time = end-start
        print(f'Insertions took {insertions_time} seconds')

    with open('./transactions/query.txt', 'r') as f:
        lines = f.readlines()
        start = time()
        for line in lines:
            key = line.split('\n')[0]
            query(key, choice(ports))
        end = time()
        queries_time = end-start
        print(f'Queries took {queries_time} seconds')


    print(f'Insertions: {insertions_time}\nQueries: {queries_time}', file = output_file)


if __name__ == '__main__':
    test12()
    # test3()
