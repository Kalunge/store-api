from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field cannot be left blank'
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'that item does not exist'}, 404

    @classmethod
    def find_by_name(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        if row:
            return {'item':{'name':row[0], 'price':row[1]}}

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'item':f'an item with the name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = {
            'name' : name, 'price':data['price']
        }
        try:
            self.insert(item)
        except:
            return {'message':"somethong occurred while inserting"}, 500

        return item, 201


    @classmethod
    def insert(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        return {'message' : 'item deleted successfully'}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args() 
        updated_item = {'name' : name, 'price' : data['price']}
        item = self.find_by_name(name)
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message':'unexpected error occured inserting item'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message':'unexpected error occured updating item'}, 500
        return updated_item

    @classmethod
    def update(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
            

        

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.close()
        
        return {'items':items}

    
