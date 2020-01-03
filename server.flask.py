from flask import Flask, jsonify, request

app = Flask(__name__)

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


# the following is developed using pure Flask
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

app.run(port=5000)