from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identify

app = Flask(__name__)
app.secret_key = 'muthomi'
api = Api(app)
jwt = JWT(app, authenticate, identify)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field cannot be left blank'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items), None)
        return {'item' : item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x : x['name'] == name, items), None):
            return {'message' : f'an item with the name {name} already exists'}, 400

        data = Item.parser.parse_args()
        new_item = {
            'name' : name, 'price':data['price']
        }

        items.append(new_item)

        return new_item

    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {'message' : 'item deleted successfully'}

    def put(self, name):
        data = Item.parser.parse_args() 
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item is None:
            item = {'name' : name, 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)
        
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')




app.run(debug=True)