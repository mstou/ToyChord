import sys
import flask
from lib.constants import *
from lib.get_ip import get_ip
from flask import abort, request
from lib.id_utils import create_id

my_ip = get_ip()
port  = sys.argv[1]

app = flask.Flask(__name__)
app.config['DEBUG'] = True

my_id       = create_id(my_ip, port)
previous_id = None
next_id     = None

'''
Endpoint that a node hits if it wants to join
the system.

Parameters:
    ip  : The ip of the remote machine that wants to join the network
    port: The port that the remote machine will use to answer queries

'''
@app.route('/join', methods=['POST'])
def request_to_join():
    if (PORT not in request.args) or (IP not in request.args):
        abort(BAD_REQUEST)

    req_port = request.args.get(PORT)
    req_ip   = request.args.get(IP)

    new_key = create_id(req_ip, req_port)


app.run(port=int(port))
