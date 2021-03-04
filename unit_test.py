import pytest
from hashlib import sha1

from lib.id_utils import *
from lib.Node import Node

class TestIdUtils:
    def test_create_key(self):
        created_key = create_key('NikosKalantas')
        assert type(created_key) == type(sha1())
        digest = created_key.hexdigest()
        assert digest == '51b87e432bef56d036b1163afff051e137c16b93'
        

    def test_create_id(self):
        id = create_id('255.255.255.255', 3000)
        assert type(id) == type(sha1())

    def test_is_in_range(self):
        target = '0e8a3ad980ec179856012b7eecf4327e99cd44cd' # sha1 of 'target'
        start = '2b020927d3c6eb407223a1baa3d6ce3597a3f88d' # sha1 of 'start'
        end = '7a92f3d26362d6557d5701de77a63a01df61e57f' # sha1 of 'end'
        something = '1af17e73721dbe0c40011b82ed4bb1a7dbe3ce29' # sha1 of 'something'
        res = is_in_range(target, start, end)
        assert type(res) == bool
        res = is_in_range(something, something, something)
        assert res == True

        
class TestNode:
    ip = '127.0.0.1'
    port = '5000'
    other_ip = '255.255.255.255'
    other_port = '3000'

    def test_init(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        assert node.ip == ip
        assert node.port == port
        assert type(node.id_str) == str
    
    def test_eq(self):
        ip = '127.0.0.1'
        port = '5000'
        other_ip = '255.255.255.255'
        other_port = '3000'
        node1 = Node(ip, port)
        node2 = Node(ip, port)
        assert node1 == node2
        assert node2 == node1
        assert not node1 == 'hello'
        node3 = Node(other_ip, port)
        node4 = Node(ip, other_port)
        assert not node3 == node4
        assert not node3 == node1
        assert not node2 == node3
        assert not node4 == node2
        
    def test_ne(self):
        ip = '127.0.0.1'
        port = '5000'
        other_ip = '255.255.255.255'
        other_port = '3000'
        node1 = Node(ip, port)
        node2 = Node(ip, port)
        node3 = Node(other_ip, port)
        node4 = Node(ip, other_port)
        assert not node1 != node2
        assert node3 != node4
        assert node1 != node3
        assert node1 != node4
    
    def test_json(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        expected_json = {
            'ip': ip,
            'port': port,
            'id': node.id_str
        }
        assert node.json() == expected_json

    def test_get_address(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        assert node.get_address() == '127.0.0.1:5000'
    
    def test_get_ip(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        assert node.get_ip() == ip
    
    def test_get_port(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        assert node.get_port() == port
    
    def test_get_id_str(self):
        ip = '127.0.0.1'
        port = '5000'
        node = Node(ip, port)
        assert type(node.get_id_str()) == str
        assert node.id_str == node.get_id_str()