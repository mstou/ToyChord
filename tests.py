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

def deploy_servers():
    print('Deploying 10 servers.')
    for p in ports:
        deploy(p, K, consistency)
    print('Deployments OK')
    sleep(10)
    print_graph()

def test3():
    deploy_servers()
    with open('./transactions/requests.txt') as f:
        lines = list(map(lambda x: x.strip('\n'), f.readlines()))
        request_times = []
        for line in lines:
            if line.startswith('insert'):
                _, key, value = line.split(', ')
                request_start = time()
                insert(key, value, choice(ports))
                request_times.append(time() - request_start)
            elif line.startswith('query'):
                _, key = line.split(', ')
                request_start = time()
                query(key, choice(ports))
                request_times.append(time() - request_start)
    test_replicas()
    print(f'Requests took {sum(request_times)} seconds')

def test12(K, consistency):
    deploy_servers()
    with open('./transactions/insert.txt', 'r') as f:
        # do all inserts and update log files
        lines = list(map(lambda line: line.strip('\n'), f.readlines()))
        insert_times = []
        for line in lines:
            key, value = line.split(', ')
            insert_start = time()
            insert(key, value, choice(ports))
            insert_end = time()
            insert_times.append(insert_end - insert_start)
        print(f'Insertions took {sum(insert_times)} seconds')

    with open('./transactions/query.txt', 'r') as f:
        query_times = []
        lines = list(map(lambda line: line.strip('\n'), f.readlines()))
        for line in lines:
            key = line.split('\n')[0]
            quey_start = time()
            query(key, choice(ports))
            query_times.append(time() - query_start)
        print(f'Queries took {sum(query_times)} seconds')


if __name__ == '__main__':
    test12()
    # test3()