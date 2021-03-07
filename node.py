import sys
import flask
import requests
import threading
from time import sleep
from lib.constants import *
from lib.get_ip import get_ip
from lib.Node import Node
from flask import abort, request, jsonify
from lib.id_utils import *
from lib.request_utils import *

# TODO: implement sys.arg flag for local testing
my_ip = get_ip(True)
my_port  = sys.argv[1]
bootstrap_node = Node('localhost', '5000')

# TODO: parse replica number from sys args
K = 3

files = {}
replicas = [{} for k in range(K-1)]

bootstrap = len(sys.argv) > 2 and sys.argv[2] == 'bootstrap'

app = flask.Flask(__name__)
# app.config['DEBUG'] = True

me       = Node(my_ip, my_port)
previous = None
next     = None

if bootstrap:
    previous = me
    next     = me

@app.route('/log', methods=['GET'])
def log():
    result = {
        'me': me.json(),
        'previous': previous.json(),
        'next': next.json(),
        'files': files,
        'replicas': replicas
    }
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

    previous = Node(previous_ip, previous_port)
    next     = Node(next_ip, next_port)

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

    next = Node(new_ip, new_port)

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

    previous = Node(new_ip, new_port)

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

    if x <= K-2:
        replicas[K-2] = {}

        for i in range(K-2, x, -1):
            replicas[i] = replicas[i-1]

        replicas[x] = {}

    return OK
'''
Insert a new replica

Parameters:
        number: the replica number
        key   : the file's name
        value : the file
'''
@app.route('/insert_replica')
def insert_replica():

    if (NUMBER not in request.args) or\
       (KEY not in request.args) or\
       (VALUE not in request.args):
        abort(BAD_REQUEST)


    key_str  = request.args.get(KEY)
    value    = request.args.get(VALUE)
    number   = int(request.args.get(NUMBER))
    key_hash = create_key(key_str).hexdigest()

    if number >= K-1:
        return OK

    replicas[number][key_hash] = {'name': key_str, 'value': value}

    insert_replica_request(next, key_str, value, number+1)

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

    if bootstrap and previous == me and next == me:
        previous = Node(req_ip, req_port)
        next     = Node(req_ip, req_port)
        sleep(1)
        join_successful_request(requester, me, me)

    # Checking if the new node is between us and the node after us
    elif is_in_range(new_id.hexdigest(), previous.get_id_str(), me.get_id_str()):
        # Notify previous to update next
        update_next_request(previous, req_port, req_ip, me.get_id_str())
        join_successful_request(requester, previous, me)

        new_previous = Node(req_ip, req_port)
        keys_to_delete = []

        for key_hash in files:
            if is_in_range(key_hash,  previous.get_id_str(), new_previous.get_id_str()):
                insert_request(new_previous, files[key_hash]['name'], files[key_hash]['value'])
                keys_to_delete.append(key_hash)

        for key_hash in keys_to_delete:
            del files[key_hash]

        previous = new_previous

    else:
        # Propagate the join request to next_id
        join_request(next, req_port, req_ip)

    return OK

'''
Endpoint that someone hits if they want to insert a file to ToyChord.
If the key does not belong to the keys the node is holding, the request
is propagated to the next node.

Parameters:
    key: The file's title
    value: File's location
'''
@app.route('/insert', methods=['GET'])
def insert():
    if (KEY not in request.args) or (VALUE not in request.args):
        abort(BAD_REQUEST)

    key_str  = request.args.get(KEY)
    value    = request.args.get(VALUE)
    key_hash = create_key(key_str)

    if is_in_range(key_hash.hexdigest(), previous.get_id_str(), me.get_id_str()):
        files[key_hash.hexdigest()] = {'name': key_str, 'value': value}
        insert_replica_request(next, key_str, value, 0)

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

        if key_hash_str in files:
            del files[key_hash_str]

    else:
        # Propagate request to next node
        delete_request(next, key_str)

    return OK

'''
Returns all files and the pointer to the next node.
'''
@app.route('/get_all_files', methods=['GET'])
def get_all_files():
    result = {}
    result['files'] = files
    result['next'] = {'port': next.get_port(), 'ip': next.get_ip()}

    return jsonify(result)

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
        next_to_query = next
        all_files = {}

        while next_to_query != me:
            response = get_all_files_request(next_to_query).json()
            next_to_query = Node(response['next']['ip'], response['next']['port'])

            all_files = {**all_files, **response['files']}

        all_files = {**all_files, **files}
        return jsonify(list(all_files.values()))

    if is_in_range(key_hash_str, previous.get_id_str(), me.get_id_str()):

        if key_hash_str in files:
            return jsonify(files[key_hash_str])

        return jsonify({})

    # Propagate request
    result = query_request(next, key_str)

    return result.json()

@app.route('/depart', methods=['GET'])
def depart():

    update_prev_request(next, previous.get_port(), previous.get_ip(), me.get_id_str())
    update_next_request(previous, next.get_port(), next.get_ip(), me.get_id_str())

    all_keys = []

    for key_hash in files:
        insert_request(next, files[key_hash]['name'], files[key_hash]['value'])
        all_keys.append(key_hash)

    for key_hash in all_keys:
        del files[key_hash]

    return OK

if not bootstrap:
    t = threading.Thread(target=join_request, args=(bootstrap_node, my_port, my_ip))
    t.start()

app.run(port=int(my_port))
