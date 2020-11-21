from random import choice, random
from time import time

import hashlib


class Hashgraph:
    NODES = []

    def __init__(self):
        pass

    def create_node(self, data: dict):
        node = {
            'id': self.encrypt(str(random() * time())),
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login']) + self.encrypt(data['password']),
            # 'previous_hash': self.NODES[-1]['id'] if self.NODES > 0 else None,
            'awareness_nodes': [],
        }
        # node['id'] = self.encrypt(str(node)) if node['previous_instance'] == None else node['id']
        node['previous_instance'] = self.find_by_id(node['id'])
        node['awareness_nodes'].append(self.find_by_id(node['id']))
        try:
            [node['awareness_nodes'].append(id_) for id_ in self.graph_consensus(node['id'])]
        except TypeError as e:
            print(e)
            pass
        self.NODES.append(node)

    @staticmethod
    def encrypt(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def graph_consensus(self, parent_id):
        if len(self.NODES) == 0 or len(self.get_unique_users()) < 2:
            return None
        parent_nodes = []
        awareness_node = choice(self.NODES)
        while awareness_node['id'] == parent_id:
            awareness_node = choice(self.NODES)
        parent_nodes.append(awareness_node['id'])
        if len(awareness_node['awareness_nodes']) > 1:
            for id_ in awareness_node['awareness_nodes'][1:]:
                parent_nodes.append(id_)
        return parent_nodes

    def get_unique_users(self):
        unique_users = []
        [unique_users.append(node) for node in self.NODES if node not in unique_users]
        return unique_users

    def find_by_id(self, id):
        for node in reversed(self.NODES):
            if node['id'] == id:
                return node
        return None


graph = Hashgraph()
graph.create_node({'login': 'Sasha', 'password': 'JavaMan'})
graph.create_node({'login': 'Egor', 'password': '2223404'})
graph.create_node({'login': 'Slava', 'password': 'PITON-GOVNO'})
graph.create_node({'login': 'Qverty', 'password': '123456'})
graph.create_node({'login': 'Asdfgh', 'password': '456789'})
graph.create_node({'login': 'Zxcvbn', 'password': '789123'})

[print(i) for i in graph.NODES]
