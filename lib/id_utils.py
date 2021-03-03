from hashlib import sha1

def create_key(key):
    return sha1(key.encode('utf-8'))

def create_id(ip, port):
    return sha1(f'{ip}:{port}'.encode('utf-8'))

def is_in_range(target, start, end):
    targetInt  = int(target, 16)
    startInt   = int(start, 16)
    endInt     = int(end, 16)

    if startInt == endInt:
        return True

    if targetInt > startInt and targetInt <= endInt:
        return True

    if startInt > endInt and targetInt <= endInt:
        return True

    if startInt >= endInt and targetInt > startInt:
        return True

    return False
