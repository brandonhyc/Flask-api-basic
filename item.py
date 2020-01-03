import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name cannot be left blank!"
    ).add_argument(
        'price',
        type=str,
        required=True,
        help="Price cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item is not None:
            return item

        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row is not None:
            return {'item': {'itemId': row[0], 'name': row[1], 'price': row[2]}}

    def post(self, name):
        data = self.parser.parse_args()
        item = (data['name'], data['price'])

        if self.find_by_name(data['name']) is not None:
            return {'message': "Item already exists"}, 400

        try:
            self.insert(item)
        except:
            return {'message': "An error occurred innserting the item."}, 500

        return {"message": "Item created successfully. name: {}, price: {}".format(data['name'], data['price'])}, 201

    def put(self, name):
        data = self.parser.parse_args()

        item = self.find_by_name(data['name'])
        updated_item = data

        try:
            if item is None:
                self.insert(updated_item)
            else:
                self.update(updated_item)
        except:
            return {'message': "An error occurred updating the item."}, 500

        return item

    @classmethod
    def update(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items set price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def insert(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        if self.find_by_name(name) is None:
            return {'message': "Item not exists"}, 400

        query = "DELECT FROM items WHERE name=?"
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        return {'message': 'DELETED Item {}'.format(name)}, 201



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'itemId': row[0], 'name': row[1], 'price': row[2]})

        connection.close()
        return {'items': items}
