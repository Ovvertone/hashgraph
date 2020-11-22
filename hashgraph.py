from random import choice, random
from time import time

import hashlib


class Hashgraph:
    NODES = []

    def __init__(self):
        pass

    def create_node(self, data: dict) -> None:
        node = {
            'id': self.encrypt(str(random() * time())),
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login'] + data['password']),
            'awareness_nodes': [],
        }
        if self.find_by_id(node['id']) is not None:
            node['awareness_nodes'].append(self.find_by_id(node['id']))
        if self.find_parent_node(node['id']) is not None:
            node['awareness_nodes'].append(self.find_parent_node(node['id']))
        node['previous_instance'] = self.encrypt(str(self.find_by_id(node['id']))) if self.find_by_id(node['id']) != None else 'genesis'
        if len(node['awareness_nodes']) != 0:
            self.aware_nodes(node['awareness_nodes'][-1], node['id'])
        self.NODES.append(node)

    def update_node(self, data: dict) -> None:
        node = {
            'id': data['id'],
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login'] + data['password']),
            'awareness_nodes': [],
        }
        node['awareness_nodes'].append(self.find_by_id(node['id'])['id'])
        if self.find_parent_node(node['id']) is not None:
            node['awareness_nodes'].append(self.find_parent_node(node['id']))
        node['previous_instance'] = self.encrypt(str(self.find_by_id(node['id'])))
        if len(node['awareness_nodes']) != 1:
            self.aware_nodes(node['awareness_nodes'][-1], node['id'])
        self.NODES.append(node)

    @staticmethod
    def encrypt(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def find_parent_node(self, parent_id: str) -> str:
        if len(self.NODES) == 0 or len(self.get_unique_users()) < 2:
            return None
        parent_node = choice(self.NODES)
        while parent_node['id'] == parent_id:
            parent_node = choice(self.NODES)
        return parent_node['id']

    def aware_nodes(self, parent_node_id: str, new_node_id: str) -> None:
        aware_node = self.find_by_id(parent_node_id)
        aware_node['awareness_nodes'].append(new_node_id)
        count_nodes = len(aware_node['awareness_nodes'])
        if count_nodes != 1:
            [self.aware_nodes(aware_node['awareness_nodes'][id_], new_node_id) for id_ in range(-2, 0, -1) if id_ != new_node_id]

    def get_unique_users(self) -> list:
        unique_users = []
        [unique_users.append(node) for node in self.NODES if node not in unique_users]
        return unique_users

    def find_by_id(self, id_: str) -> dict:
        for node in reversed(self.NODES):
            if node['id'] == id_:
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
