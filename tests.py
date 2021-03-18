from time import time
import sys
from random import randrange, choice
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

    f = open('transactions/insert.txt', 'r').read().split('\n')[:-1]

    insertions = list(map(lambda x: x.split(', '), f))

    print(f'Doing {len(insertions)} insert requests..')

    start = time()

    for q in insertions:
        name  = q[0]
        value = q[1]

        target_port = ports[randrange(0,len(ports))]
        insert(name, value, target_port)

    end = time()
    print(f'Insertions took {end-start} seconds')
    test_replicas()


if __name__ == '__main__':
    test12()
    # test3()