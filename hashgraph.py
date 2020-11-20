from random import choice
from time import time

import hashlib


class Hashgraph:
    NODES = []

    def __init__(self):
        self.NODES.append({
            'timestamp': self.encrypt(str(time())),
            'transaction': None,
            'previous_hash': None,
            'awareness_nodes': [],
            'id': 'genesis',
        })

    def create_node(self, data: dict):
        node = {
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login']) + self.encrypt(data['password']),
            'previous_hash': self.NODES[-1]['id'],
            'awareness_nodes': [],
        }
        node['id'] = self.encrypt(str(node))
        if len(self.NODES) > 2:
            [node['awareness_nodes'].append(awareness_node_id) for awareness_node_id in self.graph_consensus()]
        self.NODES.append(node)

    @staticmethod
    def encrypt(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def graph_consensus(self):
        awareness_node_1 = choice(self.NODES[1:])
        awareness_node_2 = choice(self.NODES[1:])
        while awareness_node_1 == awareness_node_2:
            awareness_node_2 = choice(self.NODES[1:])
        return [awareness_node_1['id'], awareness_node_2['id']]


graph = Hashgraph()
graph.create_node({'login': 'Sasha', 'password': 'JavaMan'})
graph.create_node({'login': 'Egor', 'password': '2223404'})
graph.create_node({'login': 'Slava', 'password': 'PITON-GOVNO'})
graph.create_node({'login': 'Qverty', 'password': '123456'})
graph.create_node({'login': 'Asdfgh', 'password': '456789'})
graph.create_node({'login': 'Zxcvbn', 'password': '789123'})
[print(i) for i in graph.NODES]


