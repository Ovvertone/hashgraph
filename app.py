from flask import Flask, request, Response
import json
from hashgraph import Hashgraph
import jwt
from functools import wraps
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

graph = Hashgraph()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return Response(json.dumps({'message': 'Token is missing!'}), 403)
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except Exception:
            return Response(json.dumps({'message': 'Token is invalid'}), 403)
        return f(*args, **kwargs)
    return decorated


exp_token = datetime.datetime.now() + datetime.timedelta(hours=24)


@app.route('/register', methods=['POST'])
def register():
    graph.create_node({'login': request.form.get('login'), 'password': request.form.get('password')})
    res = graph.get_last_node
    return Response(json.dumps(res, indent=4), 200)


@app.route('/login', methods=['POST'])
def login():
    if graph.find_user(request.form.get('login'), request.form.get('password')):
        token = jwt.encode({'user': request.form.get('login'), 'exp': exp_token}, app.config['SECRET_KEY'])
        print(token)
        return Response(json.dumps({'token': token.decode('UTF-8')}))
    return Response('Could not verify!', 401)


if __name__ == '__main__':
    app.run()
