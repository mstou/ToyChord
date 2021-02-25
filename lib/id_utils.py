from hashlib import sha1

def create_id(ip, port):
    return sha1(f'{ip}:{port}'.encode('utf-8'))

def is_id_in_range(target, start, end):

    targetInt  = int(target.hexdigest(), 16)
    startInt   = int(start.hexdigest(), 16)
    endInt     = int(end.hexdigest(), 16)

    if targetInt > startInt and targetInt < endInt:
        return True

    if startInt > endInt and targetInt < endInt:
        return True

    if startInt > endInt and targetInt > startInt:
        return True

    return False
