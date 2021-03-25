import sys
import flask
import requests
import threading
import argparse
from time import sleep
from lib.constants import *
from lib.get_ip import get_ip
from lib.Node import Node
from flask import abort, request, jsonify
from lib.id_utils import *
from lib.request_utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap", action="store_true")
parser.add_argument("--eventual", action="store_true")
parser.add_argument("--local", action="store_true")
parser.add_argument("--port", type=int)
parser.add_argument("-k", type=int)
args = parser.parse_args()

if args.bootstrap:
    print("Bootstrap node")
print(args.port)
print(args.k)

bootstrap = args.bootstrap
my_port  = args.port
local_testing = args.local
K = args.k
consistency = EVENTUAL if args.eventual else LINEARIZABILITY

my_ip = get_ip(local = local_testing)

bootstrap_node = Node('localhost', '5000') if local_testing else Node('192.168.0.1', '5000')


files_lock = threading.Semaphore()
replicas_lock = threading.Semaphore()
pointers_lock = threading.Semaphore()

files = {}
replicas = [{} for k in range(K-1)]


app = flask.Flask(__name__)

me       = Node(my_ip, my_port)
previous = None
next     = None

if bootstrap:
    previous = me
    next     = me

@app.route('/log', methods=['GET'])
def log():
    files_lock.acquire()
    replicas_lock.acquire()
    pointers_lock.acquire()

    result = {
        'me': me.json(),
        'previous': previous.json(),
        'next': next.json(),
        'files': files,
        'replicas': replicas
    }

    files_lock.release()
    replicas_lock.release()
    pointers_lock.release()

    return jsonify(result)

@app.route('/consistency', methods=['GET'])
def consistency_request():
    result = {'k': K, 'consistency': consistency}
    return jsonify(result)

'''
Notifies us that we have been successfully added to ToyChord.

Parameters:
    next_ip
    next_port
    previous_ip
    previous_port
'''
@app.route('/join_successful', methods=['GET'])
def join_successful():
    global previous
    global next

    if (NEXT_PORT not in request.args) or (NEXT_IP not in request.args):
        abort(BAD_REQUEST)

    if (PREV_PORT not in request.args) or (PREV_IP not in request.args):
        abort(BAD_REQUEST)

    if previous != None and next != None:
        abort(BAD_REQUEST)

    next_port = request.args.get(NEXT_PORT)
    next_ip   = request.args.get(NEXT_IP)
    previous_port  = request.args.get(PREV_PORT)
    previous_ip    = request.args.get(PREV_IP)

    pointers_lock.acquire()

    previous = Node(previous_ip, previous_port)
    next     = Node(next_ip, next_port)

    pointers_lock.release()

    return OK


'''
Updates the next node pointer. The update happens
only if the current next is requesting it.

Parameters:
    ip   = The ip of the remote machine that is now our next node
    port = The port that our new next node will use to answer queries
    current_next = Id of our current next node
'''
@app.route('/update_next', methods=['GET'])
def update_next():
    global next

    if (PORT not in request.args) or\
       (IP not in request.args) or\
       (CUR_NEXT not in request.args):
        abort(BAD_REQUEST)

    new_port = request.args.get(PORT)
    new_ip   = request.args.get(IP)
    next_id  = request.args.get(CUR_NEXT)

    if next_id != next.get_id_str():
        abort(UNAUTHORIZED)

    pointers_lock.acquire()
    next = Node(new_ip, new_port)
    pointers_lock.release()

    return OK

'''
Updates the previous node pointer. The update happens
only if the current previous is requesting it.

Parameters:
    ip   = The ip of the remote machine that is now our previous node
    port = The port that our new previous node will use to answer queries
    current_next = Id of our current previous node
'''
@app.route('/update_prev', methods=['GET'])
def update_prev():
    global previous

    if (PORT not in request.args) or\
       (IP not in request.args) or\
       (CUR_PREV not in request.args):
        abort(BAD_REQUEST)

    new_port = request.args.get(PORT)
    new_ip   = request.args.get(IP)
    prev_id  = request.args.get(CUR_PREV)

    if prev_id != previous.get_id_str():
        abort(UNAUTHORIZED)

    pointers_lock.acquire()
    previous = Node(new_ip, new_port)
    pointers_lock.release()

    return OK

'''
Decrease the replica number of all the replicas that
have a replica number above x

Parameters
    number: x
'''
@app.route('/decrease_replicas_in_range')
def decrease_replicas_in_range():
    global files

    if (NUMBER not in request.args):
        abort(BAD_REQUEST)

    x = int(request.args.get(NUMBER))

    if x == K-1:
        return OK

    replicas_lock.acquire()

    if x == 0:
        files_lock.acquire()
        files = {**files, **replicas[0]}
        files_lock.release()
    else:
        replicas[x-1] = {**replicas[x-1], **replicas[x]}

    for i in range(x, K-2):
        replicas[i] = replicas[i+1]

    decrease_replicas_in_range_request(next, x+1)

    for key_hash in replicas[K-2]:
        insert_replica_request(next,
                               replicas[K-2][key_hash]['name'],
                               replicas[K-2][key_hash]['value'],
                               K-2, propagate = False)

    replicas[K-2] = {}
    replicas_lock.release()

    return OK

'''
Increase the replica number of all the replicas that
have a replica number above x

Parameters
    number: x
'''
@app.route('/increase_replicas_in_range')
def increase_replicas_in_range():

    if (NUMBER not in request.args):
        abort(BAD_REQUEST)

    x = int(request.args.get(NUMBER))

    replicas_lock.acquire()

    if x >= K-1:
        replicas_lock.release()
        return OK

    if x <= K-2:
        replicas[K-2] = {}

        for i in range(K-2, x, -1):
            replicas[i] = replicas[i-1]

        replicas[x] = {}

    replicas_lock.release()

    increase_replicas_in_range_request(next, x+1)

    return OK

'''
Increase the replica number of the file provided

Parameters
    key: the file's name
    number : the replica number
'''
@app.route('/increase_replica')
def increase_replica():

    if (KEY not in request.args):
        abort(BAD_REQUEST)

    key = request.args.get(KEY)
    key_hash = create_key(key).hexdigest()
    number = int(request.args.get(NUMBER))

    if number == K:
        return OK

    replicas_lock.acquire()

    if key_hash in replicas[K-2]:
        del replicas[K-2][key_hash]

    else:
        for i in range(K-2):
            if key_hash in replicas[i]:
                tmp = replicas[i][key_hash]
                del replicas[i][key_hash]
                replicas[i+1][key_hash] = tmp
                break

    replicas_lock.release()
    increase_replica_request(next, key, number+1)

    return OK

'''
Insert a new replica

Parameters:
        number: the replica number
        key   : the file's name
        value : the file
        propagate_replicas : Whether or not to propagate the request
'''
@app.route('/insert_replica')
def insert_replica():

    if (NUMBER not in request.args) or\
       (KEY not in request.args) or\
       (VALUE not in request.args):
        abort(BAD_REQUEST)

    propagate = PROPAGATE_REPLICAS not in request.args

    key_str  = request.args.get(KEY)
    value    = request.args.get(VALUE)
    number   = int(request.args.get(NUMBER))
    key_hash = create_key(key_str).hexdigest()

    if number >= K-1:
        return OK

    replicas_lock.acquire()
    replicas[number][key_hash] = {'name': key_str, 'value': value}

    if propagate:
        if consistency == EVENTUAL:
            updates = threading.Thread(
                        target=insert_replica_request,
                        args=(next, key_str, value, number+1)
                        )
            updates.start()
        else: # LINEARIZABILITY
            insert_replica_request(next, key_str, value, number+1)

    replicas_lock.release()
    return OK

'''
Endpoint that a node hits if it wants to join
the system.

Parameters:
    ip  : The ip of the remote machine that wants to join the network
    port: The port that the remote machine will use to answer queries

'''
@app.route('/join', methods=['GET'])
def join():
    global previous
    global next

    if (PORT not in request.args) or (IP not in request.args):
        abort(BAD_REQUEST)


    req_port  = request.args.get(PORT)
    req_ip    = request.args.get(IP)
    requester = Node(req_ip, req_port)

    new_id  = create_id(req_ip, req_port)

    pointers_lock.acquire()

    if bootstrap and previous == me and next == me:
        previous = Node(req_ip, req_port)
        next     = Node(req_ip, req_port)
        sleep(1)
        pointers_lock.release()
        join_successful_request(requester, me, me)

    # Checking if the new node is between us and the node after us
    elif is_in_range(new_id.hexdigest(), previous.get_id_str(), me.get_id_str()):
        # Notify previous to update next
        update_next_request(previous, req_port, req_ip, me.get_id_str())
        join_successful_request(requester, previous, me)

        new_previous = Node(req_ip, req_port)
        files_to_replicas = []

        files_lock.acquire()
        replicas_lock.acquire()

        for key_hash in files:
            if is_in_range(key_hash,  previous.get_id_str(), new_previous.get_id_str()):
                insert_request(new_previous, files[key_hash]['name'], files[key_hash]['value'], propagate = False)
                files_to_replicas.append(key_hash)

        replicas_exist = False

        for k in range(K-1):
            for key_hash in replicas[k]:
                replicas_exist = True
                insert_replica_request(requester,
                                       replicas[k][key_hash]['name'],
                                       replicas[k][key_hash]['value'],
                                       k,
                                       propagate = False)

        if K >= 2:
            replicas[K-2] = {}
            for i in range(K-2, 0, -1):
                replicas[i] = replicas[i-1]
            replicas[0] = {}

        if replicas_exist:
            increase_replicas_in_range_request(next,1)

        for key_hash in files_to_replicas:
            replicas[0][key_hash] = files[key_hash]
            increase_replica_request(next, files[key_hash]['name'], 1)
            del files[key_hash]


        previous = new_previous

        files_lock.release()
        replicas_lock.release()
        pointers_lock.release()

    else:
        # Propagate the join request to next_id
        pointers_lock.release()
        join_request(next, req_port, req_ip)

    return OK

'''
Endpoint that someone hits if they want to insert a file to ToyChord.
If the key does not belong to the keys the node is holding, the request
is propagated to the next node.

Parameters:
    key: The file's title
    value: File's location
    propagate_replicas : Whether or not to propagate replica requests
'''
@app.route('/insert', methods=['GET'])
def insert():
    if (KEY not in request.args) or (VALUE not in request.args):
        abort(BAD_REQUEST)

    propagate = PROPAGATE_REPLICAS not in request.args

    key_str   = request.args.get(KEY)
    value     = request.args.get(VALUE)
    key_hash  = create_key(key_str)

    if is_in_range(key_hash.hexdigest(), previous.get_id_str(), me.get_id_str()):

        files_lock.acquire()
        files[key_hash.hexdigest()] = {'name': key_str, 'value': value}

        if propagate and K > 1:
            if consistency == EVENTUAL:
                updates = threading.Thread(
                                target=insert_replica_request,
                                args=(next, key_str, value, 0)
                                )
                updates.start()
            else: # LINEARIZABILITY
                insert_replica_request(next, key_str, value, 0)

        files_lock.release()

    else:
        # Propagate request to next node
        insert_request(next, key_str, value)

    return OK

'''
Endpoint that someone hits if they want to delete a file from ToyChord.
If the key does not belong to the keys the node is holding, the request
is propagated to the next node.

Parameters:
    key: The file's title
'''
@app.route('/delete', methods=['GET'])
def delete():
    if (KEY not in request.args):
        abort(BAD_REQUEST)

    key_str  = request.args.get(KEY)
    key_hash = create_key(key_str)

    if is_in_range(key_hash.hexdigest(), previous.get_id_str(), me.get_id_str()):
        key_hash_str = key_hash.hexdigest()

        files_lock.acquire()

        if key_hash_str in files:
            if K > 1:
                if consistency == EVENTUAL:
                    threading.Thread(
                                target=delete_replica_request,
                                args=(next, files[key_hash_str]['name'], 0)
                                ).start()
                else: # LINEARIZABILITY
                    delete_replica_request(next, files[key_hash_str]['name'], 0)

            del files[key_hash_str]

        files_lock.release()

    else:
        # Propagate request to next node
        delete_request(next, key_str)

    return OK

'''
Delete a replica of a file

Parameters:
    key    : The file's title
    number : The replica number of the file
'''
@app.route('/delete_replica', methods=['GET'])
def delete_replica():
    if (KEY not in request.args):
        abort(BAD_REQUEST)

    key_str  = request.args.get(KEY)
    key_hash = create_key(key_str).hexdigest()
    number   = int(request.args.get(NUMBER))

    if number > K-1 or number < 0:
        abort(BAD_REQUEST)

    if number == K-1:
        return OK

    replicas_lock.acquire()

    if key_hash in replicas[number]:
        del replicas[number][key_hash]
        delete_replica_request(next, key_str, number+1)

    replicas_lock.release()

    return OK

'''
Returns all files and the pointer to the next node.
'''
@app.route('/get_all_files', methods=['GET'])
def get_all_files():
    replicas_lock.acquire()
    pointers_lock.acquire()

    result = {}
    result['files'] = files if K == 1 else replicas[K-2]
    result['next'] = {'port': next.get_port(), 'ip': next.get_ip()}

    replicas_lock.release()
    pointers_lock.release()

    return jsonify(result)

'''
Queries a key from a replica

Parameters:
    key = the key we are searching for
    number = the replica we are looking for
'''
@app.route('/query_replica', methods=['GET'])
def query_replica():
    if (KEY not in request.args) or (NUMBER not in request.args):
        abort(BAD_REQUEST)

    key_str  = request.args.get(KEY)
    key_hash = create_key(key_str)
    key_hash_str  = key_hash.hexdigest()
    number = int(request.args.get(NUMBER))

    print(f'{me} just got a replica query')
    if number < K-1:
        result = query_replica_request(next, key_str, number+1)
        return result.json()

    if number == K-1:
        replicas_lock.acquire()
        file = replicas[K-2][key_hash_str]
        replicas_lock.release()

        return jsonify(file)

'''
Queries a key

Parameters:
    key = the key we are searching for
'''
@app.route('/query', methods=['GET'])
def query():
    if (KEY not in request.args):
        abort(BAD_REQUEST)

    key_str  = request.args.get(KEY)
    key_hash = create_key(key_str)
    key_hash_str  = key_hash.hexdigest()

    if key_str == '*':
        # Gather all files from all nodes
        files_lock.acquire()
        replicas_lock.acquire()
        pointers_lock.acquire()

        next_to_query = next
        my_files = {
                'me': me.json(),
                'previous': previous.json(),
                'next': next.json(),
                'files': files,
                'replicas': replicas
                }

        files_lock.release()
        replicas_lock.release()
        pointers_lock.release()
        all_files = [my_files]

        while next_to_query != me:
            response = log_request(next_to_query).json()
            next_to_query = Node(response['next']['ip'], response['next']['port'])

            all_files.append(response)

        return jsonify(all_files)

    pointers_lock.acquire()

    if is_in_range(key_hash_str, previous.get_id_str(), me.get_id_str()):

        files_lock.acquire()
        pointers_lock.release()

        if key_hash_str in files:

            if consistency == EVENTUAL or K == 1:
                result = files[key_hash_str]
                files_lock.release()

            else: # LINEARIZABILITY
                files_lock.release()
                print(f'{me} querying replica')
                result = query_replica_request(next, key_str, 1).json()

            return jsonify(result)

        files_lock.release()
        return jsonify({})

    next_ = next
    pointers_lock.release()

    if consistency == EVENTUAL and K > 1:
        replicas_lock.acquire()
        for i in range(K-1):
            if key_hash_str in replicas[i]:
                result = replicas[i][key_hash_str]
                replicas_lock.release()
                return jsonify(result)

        replicas_lock.release()


    # Propagate request
    result = query_request(next_, key_str)

    return result.json()

@app.route('/depart', methods=['GET'])
def depart():
    files_lock.acquire()
    replicas_lock.acquire()
    pointers_lock.acquire()

    update_prev_request(next, previous.get_port(), previous.get_ip(), me.get_id_str())
    update_next_request(previous, next.get_port(), next.get_ip(), me.get_id_str())


    for key_hash in list(files.keys()):
        del files[key_hash]

    decrease_replicas_in_range_request(next, 0)

    if K == 1:
        for key_hash_str in files:
            insert_request(next,
                           files[key_hash_str]['name'],
                           files[key_hash_str]['value'],
                           propagate = False)
    else:
        for key_hash in replicas[K-2]:
            insert_replica_request(next,
                                   replicas[K-2][key_hash]['name'],
                                   replicas[K-2][key_hash]['value'],
                                   K-2, propagate = False)

    files_lock.release()
    replicas_lock.release()
    pointers_lock.release()

    return OK

if not bootstrap:
    t = threading.Thread(target=join_request, args=(bootstrap_node, my_port, my_ip))
    t.start()

app.run(host='0.0.0.0', port=int(my_port))
