from hashlib import sha1

def create_id(ip, port):
    return sha1(f'{ip}:{port}'.encode('utf-8'))

def is_id_in_range(target, start, end):
    raise NotImplementedError
