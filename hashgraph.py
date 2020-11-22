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
            'transaction': self.encrypt(data['login'] + data['password']),
            'awareness_nodes': [],
        }
        if self.find_by_id(node['id']) is not None:
            node['awareness_nodes'].append(self.find_by_id(node['id']))
        if self.parent_nodes(node['id']) is not None:
            node['awareness_nodes'].append(self.parent_nodes(node['id']))
        node['previous_instance'] = self.encrypt(str(self.find_by_id(node['id']))) if self.find_by_id(node['id']) != None else 'genesis'
        self.NODES.append(node)

    def update_node(self, data: dict):
        node = {
            'id': data['id'],
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login'] + data['password']),
            'awareness_nodes': [],
        }
        if self.find_by_id(node['id']) is not None:
            node['awareness_nodes'].append(self.find_by_id(node['id'])['id'])
        node['awareness_nodes'].append(self.parent_nodes(node['id']))
        node['previous_instance'] = self.encrypt(str(self.find_by_id(node['id']))) if self.find_by_id(node['id']) is not None else None
        self.NODES.append(node)

    @staticmethod
    def encrypt(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def parent_nodes(self, parent_id: str) -> str:
        if len(self.NODES) == 0 or len(self.get_unique_users()) < 2:
            return None
        awareness_node = choice(self.NODES)
        while awareness_node['id'] == parent_id:
            awareness_node = choice(self.NODES)
        return awareness_node['id']

    def aware_nodes(self, node: dict):
        pass

    def get_unique_users(self) -> list:
        unique_users = []
        [unique_users.append(node) for node in self.NODES if node not in unique_users]
        return unique_users

    def find_by_id(self, id: str) -> str:
        for node in reversed(self.NODES):
            if node['id'] == id:
                return node

    @property
    def get_last_node(self) -> dict:
        return self.NODES[-1]

    def find_user(self, login: str, password: str) -> bool:
        hashed_logpass = self.encrypt(login + password)
        for node in self.NODES:
            if node['transaction'] == hashed_logpass:
                return True
        return False


graph = Hashgraph()
graph.create_node({'login': 'Sasha', 'password': 'JavaMan'})
graph.create_node({'login': 'Egor', 'password': '2223404'})
graph.create_node({'login': 'Slava', 'password': 'PITON-GOVNO'})
graph.create_node({'login': 'Qverty', 'password': '123456'})
graph.create_node({'login': 'Asdfgh', 'password': '456789'})
graph.create_node({'login': 'Zxcvbn', 'password': '789123'})

graph.update_node({'id': graph.NODES[1]['id'], 'login': 'Ivan', 'password': '321123321'})
[print(i) for i in graph.NODES]
