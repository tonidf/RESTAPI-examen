import json
from operator import methodcaller
import os
from turtle import update 
from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_mysqldb import MySQL
from config import config



MONGO_URI=os.getenv('MONGO_URI')

mongo = MongoClient(MONGO_URI)
app = Flask(__name__)

db = MySQL(app)


@app.route('/')
def get_users_s():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    datos = cursor.fetchall()

    return jsonify(datos)

@app.route('/add_user', methods=['POST'])
def add_user():

    username = request.json.get('username')
    phone = request.json.get('phone')
    email = request.json.get('email')

    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO contacts (email, username, phone) VALUES (%s, %s, %s)',(email, username, phone))
    db.connection.commit()

    return jsonify("Usuario añadido correctamente")

@app.route('/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    cursor = db.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = %s', (id,))
    db.connection.commit()

    return jsonify('Usuario elimindado correctamente')

@app.route('/update_user_s/<id>', methods=['PUT'])
def update_user_s(id):

    username = request.json.get('username')
    phone = request.json.get('phone')
    email = request.json.get('email')

    cursor = db.connection.cursor()
    cursor.execute('UPDATE contacts SET username = %s, email = %s, phone = %s WHERE id = %s',(username, email, phone, id))
    db.connection.commit()

    return jsonify('Usuario actualizado correctamente')

@app.route('/add_user_m', methods=['POST'])
def mongo_add():
    username = request.json.get('username')
    phone = request.json.get('phone')
    email = request.json.get('email')

    mongo.db.contacts.insert_one({"username": username, "phone": phone, "email": email})

    return jsonify("Añadido correctamente")

@app.route('/get_user/<id>', methods=['GET'])
def get_user_m(id):
    user = mongo.db.contacts.find_one({"_id": ObjectId(id)})

    return jsonify(user)

@app.route('/update_user_m/<id>', methods=['UPDATE'])
def update_user(id):
    username = request.json.get('username')
    phone = request.json.get('phone')
    email = request.json.get('email')    
    data = {"username": username, "phone": phone, "email": email}

    updated = mongo.db.contacts.update_one({"_id": ObjectId(id)}, {"$set": data})

    return jsonify(updated)

@app.route('/delete_m/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.contacs.delete_one({"_id": ObjectId(id)})
    return jsonify("Usuario borrado directamente")

if __name__ == '__main__':

    app.config.from_object(config['production'])
    app.run(debug=True, host='0.0.0.0')