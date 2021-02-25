import sys
import flask
from hashlib import sha1
from lib.get_ip import get_ip

my_ip = get_ip()
port  = sys.argv[1]

app = flask.Flask(__name__)
app.config['DEBUG'] = True

my_key       = sha1(f'{my_ip}:{port}'.encode('utf-8'))
previous_key = None
next_key     = None

'''
Endpoint that a node hits if it wants to join
the system.
'''
@app.route('/join', methods=['POST'])
def request_to_join():
    raise NotImplementError

app.run(port=int(port))
