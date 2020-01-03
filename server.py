from datetime import timedelta

from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'CHANGE'
api = Api(app)

jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=18000)

# the following is developed using Flask-restful
class Student(Resource):
    def get(self, name):
        return {'student': name}

    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append

class _Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda it: it['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        item = next(filter(lambda it: it['name'] == name, items), None)
        if item is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = _Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = _Item.parser.parse_args()
        item = next(filter(lambda it: it['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


api.add_resource(Student, '/student_deprecated/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

#--------------------------------------------------
# the following is developed using pure Flask
# NOT USED

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name' : 'My Item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/') # 'http://www.google.com'
def home():
    return "Hello, world"

@app.route('/store/<string:name>') #http://localhost:5000/store/some_name
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({
        'stores': stores
    })

@app.route('/store', methods=['POST'])
def create_stores():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    if name not in stores:
        return jsonify({'massage': 'store not found'})
    new_item = {
        'name': request_data['name'],
        'price': request_data['price']
    }

    stores[name].append(new_item)
    return jsonify(new_item)

if __name__ == '__main__':
    app.run(port=5000, debug=True)