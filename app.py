from random import choice
from time import time

import hashlib


class Hashgraph:
    NODES = []

    def __init__(self):
        pass

    @staticmethod
    def encrypt(value: str) -> str:
        return hashlib.md5(value.encode()).hexdigest()

    def create_node(self, data: dict) -> None:
        self.NODES.append({
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(data['login'] + data['password']),
            'parent_node': None,
            'awareness_node': None if len(self.NODES) == 0 else self.encrypt(choice(str(self.NODES))),
        })

    def update_node(self, old_data: dict, new_data: dict) -> None:
        old_transaction = self.encrypt(old_data['login'] + old_data['password'])
        while awareness_node := choice(self.NODES)['transaction'] == old_transaction:
            continue
        node = {
            'timestamp': self.encrypt(str(time())),
            'transaction': self.encrypt(new_data['login'] + new_data['password']),
            'parent_node': self.encrypt(str(self.find_by_transaction(old_transaction))),
            'awareness_node': self.encrypt(str(awareness_node)),
        }
        self.NODES.append(node)

    def find_by_transaction(self, transaction: str) -> dict:
        for node in reversed(self.NODES):
            if node['transaction'] == transaction:
                return node

    def get_unique_users(self) -> list:
        unique_users = []
        [unique_users.append(node) for node in self.NODES if node not in unique_users]
        return unique_users

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
graph.create_node({'login': 'Qwerty', 'password': '123456'})
graph.create_node({'login': 'John Doe', 'password': '112233'})

graph.update_node({'login': 'Qwerty', 'password': '123456'}, {'login': 'Ivan', 'password': '321123321'})
[print(i) for i in graph.NODES]
