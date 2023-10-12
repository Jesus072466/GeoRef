from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import math

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
db = SQLAlchemy(app)

class Atractive(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    img = db.Column(db.String(250))
    id_detail = db.Column(db.Integer)
    id_author = db.Column(db.Integer)
    id_category = db.Column(db.Integer)
    id_coordinates = db.Column(db.Integer)
    id_mac_address = db.Column(db.Integer)
    
class Coordenates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())

class Detail_Atractive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    technique = db.Column(db.String(250))
    material = db.Column(db.String(250))
    sizes = db.Column(db.String(250))
    style = db.Column(db.String(250))
    city = db.Column(db.String(250))
    country = db.Column(db.String(250))
    address = db.Column(db.String(250))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))

class MAC_Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(250))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    birthday = db.Column(db.String(250))
    death = db.Column(db.String(250))
    description = db.Column(db.String(250))
    img = db.Column(db.String(250))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "_main_":
    with app.app_context:
        db.create_all()

    app.run(debug=True)
