from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(128))
    token = db.Column(db.String(64))

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())

class DistanceStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idReference = db.Column(db.Integer)
    idReference2 = db.Column(db.Integer)
    distance = db.Column(db.Float())

class Productos(db.Model):
    idProduct = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    name = db.Column(db.String(100))

class Product_detail(db.Model):
    idDetail = db.Column(db.Integer, primary_key=True)
    idProduct = db.Column(db.Integer)
    idStore = db.Column(db.Integer)
    price = db.Column(db.Float())
    stock = db.Column(db.Integer)
    
def get_distance(lat1, lng1, lat2, lng2):
    #print(lat1, lat2, lng1, lng2)
    lat1, lat2, lng1, lng2 = map(math.radians, [float(lat1), float(lat2), float(lng1), float(lng2)])

    dlat = lat2 - lat1
    dlon = lng2 - lng1

    a = math.sin(float(dlat)/2)**2 + math.cos(float(lat1)) * math.cos(float(lat2)) * math.sin(float(dlon)/2)**2
    c = 2 * math.asin(math.sqrt(a))

    R = 6371.0
    distancia = R * c

    return distancia

# Función para obtener los detalles de un producto
def get_product_details(idStore):
    detailsList = []

    if idStore == 200:
        d = Product_detail.query.filter_by(idStore=idStore).first()
        detailsList.append({
            'idDetail': d.idDetail,
            'idProduct': d.idProduct,
            'idStore': d.idStore,
            'price': d.price,
            'stock': d.stock
        })

    return detailsList

# Función para obtener las tiendas más cercanas
def get_nearest_stores(lat, lng, stores, num):
    nearest_stores = []

    for store in stores:
        new_dis = get_distance(lat, lng, store.lat, store.lng)
        nearest_stores.append({
            'id': store.id,
            'name': store.name,
            'distance_km': new_dis
        })

    nearest_stores.sort(key=lambda x: x['distance_km'])

    return nearest_stores[:num]

@app.route('/')
def index():
    edad = 18
    #return "<h1>Index</h1>"
    return render_template('index.html', edad = edad)

@app.route('/mapa/<float:lat>/<float:long>/<string:texto>')
def mapa(lat, long, texto):
    return render_template('mapa.html', lat = lat, long = long, texto = texto)

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        if user.token == "":
            token = secrets.token_hex(32)
            user.token = token
            db.session.commit()

        return jsonify({'name':user.name,'token':user.token})
    else :
        return jsonify({'error':'Credenciales inválidas'})

@app.route('/datos',methods=['GET'])
def getDatos():
    try:
        data = request
        return jsonify({data})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/get_store',methods=['POST'])
def get_Store():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    name = data.get('name')

    stores = Store.query.all()
    prev_distance = 9999999
    nearest_store = None

    for store in stores:
        new_dis = get_distance(lat, lng, store.lat, store.lng)
        if new_dis < prev_distance:
            prev_distance = new_dis
            nearest_store = store

    return jsonify({"datos" : nearest_store.name})

@app.route('/get_products/', methods=['POST'])
def get_products():
    try:
        data = request.get_json()
        idStore = data.get('id')

        storeOne = Store.query.filter_by(id=idStore).first()
        lat = storeOne.lat
        lng = storeOne.lng
        num = 4

        stores = Store.query.all()

        nearest_stores = get_nearest_stores(lat, lng, stores, num)
        detailsList = get_product_details(idStore)

        for sotreNum in nearest_stores:
            details = Product_detail.query.filter_by(idStore=sotreNum['id']).all()
            for d in details:
                detailsList.append({
                    'idDetail': d.idDetail,
                    'idProduct': d.idProduct,
                    'idStore': d.idStore,
                    'price': d.price,
                    'stock': d.stock
                })

        return jsonify(detailsList)
    except:
        return jsonify({"error": "Error al recibir los datos"})

if __name__ == "_main_":
    with app.app_context:
        db.create_all()

    app.run(debug=True)