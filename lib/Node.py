from lib.id_utils import create_id

class Node:
    def __init__(self, ip, port):
        self.id     = create_id(ip, port)
        self.ip     = ip
        self.port   = port
        self.id_str = self.id.hexdigest()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id_str == other.id_str
        else:
            return False

    def __str__(self):
        return f'Node listening at {self.ip}:{self.port}\n' +\
        f'Node id: {self.id_str}'
    
    def json(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'id': self.id_str
        }

    def get_address(self):
        return f'{self.ip}:{self.port}'

    def get_ip(self):
        return self.ip

    def get_id_str(self):
        return self.id_str

    def get_id(self):
        return self.id

    def get_port(self):
        return self.port
