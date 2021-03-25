import socket

def get_ip(local = False, port = 5000):

    if local:
        return '127.0.0.1'

    if port == 5000:
        return '192.168.0.1'
    if port == 3000:
        return '192.168.0.3'
    if port == 4000:
        return '192.168.0.2'
    if port == 8000:
        return '192.168.0.4'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
