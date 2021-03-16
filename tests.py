import argparse
from time import time
from random import randrange
from local_testing import *
from lib.constants import *

K = 5
consistency = LINEARIZABILITY
ports = [5000, 3000, 3030, 5050, 5051, 5055, 8000, 8080, 8081, 9000]

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
