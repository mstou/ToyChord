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

files = {}

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

        for key_hash in files:
            if is_in_range(key_hash,  previous, new_previous):
                insert_request(new_previous, files[key_hash]['name'], files[key_hash]['value'])
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

    if is_in_range(key_hash, previous.get_id(), me.get_id()):
        key_hash_str = key_hash.hexdigest()

        if key_hash_str in files:
            del files[key_hash_str]

    else:
        # Propagate request to next node
        delete_request(next, key_str)

    return OK


if not bootstrap:
    t = threading.Thread(target=join_request, args=(bootstrap_node, my_port, my_ip))
    t.start()

# TODO: we must open this in a new thread..
app.run(port=int(my_port))
