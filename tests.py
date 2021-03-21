import sys
import argparse
from tqdm import tqdm
from time import time
from random import choice
from local_testing import *
from lib.constants import *
from itertools import product

parser = argparse.ArgumentParser()
parser.add_argument("-k", type=int)
parser.add_argument("--all", action="store_true")
parser.add_argument("--eventual", action="store_true")
args = parser.parse_args()

print(args)

K = 3 if args.k == None else args.k
consistency = EVENTUAL if args.eventual else LINEARIZABILITY
run_all = args.all

ports = [5000, 3000, 3030, 5050, 5051, 5055, 8000, 8080, 8081, 9000]

all_consistencies = [EVENTUAL, LINEARIZABILITY]
all_k = list(range(1,11))

def test3(k, consistency_):
    print('Deploying 10 servers.')
    for p in ports:
        deploy(p, k, consistency_, killable = True)
    print('Deployments OK')
    sleep(10)
    print_graph()
    output_file = open(f'test_results/3/{k}_{consistency_}_{time()}', 'w')
    hashtable = {}
    stale_reads = 0
    with open('./transactions/requests.txt') as f:
        lines = list(map(lambda x: x.strip('\n'), f.readlines()))
        request_times = []
        for line in lines:
            if line.startswith('insert'):
                _, key, value = line.split(', ')
                request_start = time()
                insert(key, value, choice(ports))
                request_times.append(time() - request_start)
                hashtable[key] = value # update hashtable
            elif line.startswith('query'):
                _, key = line.split(', ')
                request_start = time()
                response = query(key, choice(ports))
                request_times.append(time() - request_start)
                if key not in hashtable:
                    pass
                else:
                    value = hashtable[key]
                    read = 'nothing' if 'value' not in response else response['value']
                    if value != read:
                        print(f"\u274c stale read for key {key}. Expected {value}, got {read}")
                        stale_reads += 1
    test_replicas()
    print(f'Requests took {sum(request_times)} seconds')
    print(f'{sum(request_times)}', file = output_file)
    print(f'Stale reads: {stale_reads}')
    print(f'Stale reads: {stale_reads}', file=output_file)

def test12(k, consistency_):
    print(f'Running experiment with k = {k} and consistency {consistency_}')
    output_file = open(f'test_results/{k}_{consistency_}_{time()}', 'w')
    print('Deploying 10 servers.')
    for p in ports:
        deploy(p, k, consistency_, killable = True)
    print('Deployments OK')
    sleep(10)
    print_graph()
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
            query_start = time()
            query(key, choice(ports))
            query_times.append(time() - query_start)
        print(f'Queries took {sum(query_times)} seconds')


if __name__ == '__main__':
    if run_all:
        all_configurations = product(all_consistencies, all_k, list(range(5)))

        for consistency_, k, _ in tqdm(all_configurations):
            print()
            # test12(k, consistency_)
            test3(k, consistency_)
            kill_servers()
            sleep(5)
    else:
        test12()
