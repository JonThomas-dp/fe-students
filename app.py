from flask import Flask, jsonify, request
import psycopg2
from sqlalchemy import delete
import os

from db import *
from flask_marshmallow import Marshmallow

from models.users import Users, user_schema, users_schema

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_POST")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")
database_password = os.environ.get("DATABASE_PASSWORD")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}:{database_password}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)

ma = Marshmallow(app)

@app.route('/api/users', methods=['GET'])
def get_users():
    query = db.session.query(Users).all()

    if not query:
        return jsonify("There are no records in the users table"), 400

    else:
        return jsonify({"message": "users found", "results": users_schema.dump(query)}), 200

@app.route('/api/admin/user', methods=['POST', 'DELETE'])
def crud_user(): 
    if request.method == "POST":
        data = request.form if request.form else request.json

        fields = ['name']
        required_fields = ['name']

        values = {}

        for field in fields:
            field_data = data.get(field)
            if field_data in required_fields and not field_data:
                return jsonify({"message": f'{field} is required'}), 400

            values[field] = field_data

        new_user = Users(values['name'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"user {values['name']} created"}), 200

    elif request.method == "DELETE":
        data = request.form if request.form else request.json

        fields = ['id']
        required_fields = ['id']

        values = {}

        for field in fields:
            field_data = data.get(field)
            if field_data in required_fields and not field_data:
                return jsonify({"message": f'{field} is required'}), 400
            
            values[field] = field_data
        
        query = db.session.query(Users).filter(Users.id == values['id']).first()
        if not query:
            return jsonify({"message": "user not found"}), 400
        
        db.session.delete(query)
        db.session.commit()

        return jsonify({"message": "user deleted", "results": user_schema.dump(query)}), 200

def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created")

create_tables()

if __name__ == '__main__':
    app.run(host=flask_host, port=flask_port)