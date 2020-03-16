import sqlite3
from flask_restful import Resource, reqparse

class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()

        return user


    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = ("SELECT * FROM users WHERE id=?")
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user=None

        conn.close()

        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str, 
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument('password',
        type=str, 
        required=True,
        help='This field cannot be left blank'
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message':'a username by that name already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users Values(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        
        return {'message':'user successfullt created'}, 201
        
        


