import sys
import flask
import requests
import threading
from time import sleep
from lib.constants import *
from lib.get_ip import get_ip
from lib.Node import Node
from flask import abort, request
from lib.id_utils import create_id, is_id_in_range
from lib.request_utils import *

my_ip = get_ip(True)
my_port  = sys.argv[1]
bootstrap_node = Node('localhost', '5000')

bootstrap = len(sys.argv) > 2 and sys.argv[2] == 'bootstrap'

app = flask.Flask(__name__)
# app.config['DEBUG'] = True

me       = Node(my_ip, my_port)
previous = None
next     = None

@app.route('/log', methods=['GET'])
def log():
    return f'Myself: {me}<br/><br/>Next: {next}<br/><br/>Previous: {previous}'

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
        print('here 1')
        abort(BAD_REQUEST)

    if (PREV_PORT not in request.args) or (PREV_IP not in request.args):
        print('here 1')
        abort(BAD_REQUEST)

    if previous != None and next != None:
        print('here 2')
        abort(BAD_REQUEST)

    next_port = request.args.get(NEXT_PORT)
    next_ip   = request.args.get(NEXT_IP)
    previous_port  = request.args.get(PREV_PORT)
    previous_ip    = request.args.get(PREV_IP)

    previous = Node(previous_ip, previous_port)
    next     = Node(next_ip, next_port)

    return OK


'''
Updates the previous node pointer. The update happens
only if the current previous is requesting it.

Parameters:
    ip   = The ip of the remote machine that is now our previous node
    port = The port that our new previous node will use to answer queries
    current_previous = Id of our current previous node
'''
@app.route('/update_previous', methods=['GET'])
def update_previous():
    global previous

    if (PORT not in request.args) or\
       (IP not in request.args) or\
       (CUR_PREVIOUS not in request.args):
        abort(BAD_REQUEST)

    new_port = request.args.get(PORT)
    new_ip   = request.args.get(IP)
    prev_id  = request.args.get(CUR_PREVIOUS)

    if prev_id != previous.get_id_str():
        abort(UNAUTHORIZED)

    previous = Node(new_ip, new_port)


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

    if bootstrap and previous == None and next == None:
        print('Case 1\n')
        previous = Node(req_ip, req_port)
        next     = Node(req_ip, req_port)
        sleep(2)
        join_successful_request(requester, me, me)

    # Checking if the new node is between us and the node after us
    elif is_id_in_range(new_id, me.get_id(), next.get_id()):
        print('Case 2\n')
        # Notify next to update previous
        update_previous_request(next, req_port, req_ip, me.get_id_str())
        join_successful_request(requester, me, next)

        next = Node(req_ip, req_port)

    else:
        print('Case 3\n')
        # Propagate the join request to next_id
        join_request(next, req_port, req_ip)

    return OK

if not bootstrap:
    t = threading.Thread(target=join_request, args=(bootstrap_node, my_port, my_ip))
    t.start()

# TODO: we must open this in a new thread..
app.run(port=int(my_port))
