# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chemacruzp:123qweZXC@chemacruzp.mysql.pythonanywhere-services.com:3306/chemacruzp$default'
db = SQLAlchemy(app)

# Definir modelos de base de datos utilizando SQLAlchemy

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

"""
Esta función calcula la distancia entre dos coordenadas geográficas.

URL: No aplica
Método: No aplica
"""
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


"""
Este es un comentario que describe la ruta principal de la aplicación.

URL: http://iaelchavez.pythonanywhere.com/
Método: GET
Respuesta: Página HTML renderizada con la variable 'edad'
Ejemplo de uso: Accede a la raíz de la aplicación.
"""
@app.route('/')
def index():
    edad = 18
    #return "<h1>Index</h1>"
    return render_template('index.html', edad = edad)

"""
Este es un comentario que describe una ruta para mostrar un mapa.

URL: http://iaelchavez.pythonanywhere.com/mapa/<float:lat>/<float:long>/<string:texto>
Método: GET
Respuesta: Página HTML renderizada con las variables 'lat', 'long', y 'texto'
Ejemplo de uso: Accede a la ruta /mapa/22.395947/-105.456117/EjemploTexto
"""
@app.route('/mapa/<float:lat>/<float:long>/<string:texto>')
def mapa(lat, long, texto):
    return render_template('mapa.html', lat = lat, long = long, texto = texto)

"""
Este es un comentario que describe una ruta para manejar la autenticación.

URL: http://iaelchavez.pythonanywhere.com/login
Método: POST
Respuesta: Objeto JSON con nombre y token si la autenticación es exitosa, o un objeto JSON de error si las credenciales son inválidas.
Ejemplo de uso: Envía una solicitud POST con datos de autenticación.
"""
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

"""
Este es un comentario que describe una ruta para obtener datos.

URL: http://iaelchavez.pythonanywhere.com/datos
Método: GET
Respuesta: Objeto JSON con los datos de la solicitud o un objeto JSON de error si ocurre una excepción.
Ejemplo de uso: Accede a la ruta /datos.
"""
@app.route('/datos',methods=['GET'])
def getDatos():
    try:
        data = request
        return jsonify({data})
    except Exception as e:
        return jsonify({'error': e})

"""
Este es un comentario que describe una ruta para obtener la tienda más cercana.

URL: http://iaelchavez.pythonanywhere.com/get_store
Método: POST
Respuesta: Objeto JSON con el nombre de la tienda más cercana.
Ejemplo de uso: Envía una solicitud POST con datos de ubicación.
"""
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

"""
Este es un comentario que describe una función para obtener detalles de un producto.

URL: No aplica
Método: No aplica
"""
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

"""
Este es un comentario que describe una función para obtener las tiendas más cercanas.

URL: No aplica
Método: No aplica
"""
def get_nearest_stores(lat, lng, stores):
    nearest_stores = []

    for store in stores:
        new_dis = get_distance(lat, lng, store.lat, store.lng)
        nearest_stores.append({
            'id': store.id,
            'name': store.name,
            'distance_km': new_dis
        })

    nearest_stores.sort(key=lambda x: x['distance_km'])

    return nearest_stores[:5]

"""
Este es un comentario que describe una función para obtener la tienda más cercana dentro de un radio específico.

URL: No aplica
Método: No aplica
"""
def get_nearest_store(lat, lng, stores, radio):
    nearest_stores = []
    nearest_store = None
    min_distance = float('inf')

    for store in stores:
        distance = get_distance(lat, lng, store.lat, store.lng)
        if distance < radio and distance < min_distance:
            min_distance = distance
            nearest_store = store

    return nearest_store, min_distance

"""
Este es un comentario que describe una ruta para obtener detalles de productos.

URL: http://iaelchavez.pythonanywhere.com/get_products/
Método: POST
Respuesta: Objeto JSON con detalles de productos o un objeto JSON de error si ocurre una excepción.
Ejemplo de uso: Envía una solicitud POST con datos de ubicación.
"""
@app.route('/get_products/', methods=['POST'])
def get_products():
    try:
        data = request.get_json()
        idStore = data.get('id')

        storeOne = Store.query.filter_by(id=idStore).first()
        lat = storeOne.lat
        lng = storeOne.lng
        num = 5

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

"""
Este es un comentario que describe una ruta para obtener la tienda más cercana actual.

URL: http://iaelchavez.pythonanywhere.com/get_current_store
Método: GET
Respuesta: Objeto JSON con la tienda más cercana o un objeto JSON de error si no se encuentra una tienda dentro del radio especificado.
Ejemplo de uso: Accede a la ruta /get_current_store con parámetros de latitud, longitud y radio.
"""
@app.route('/get_current_store', methods=['GET'])
def get_current_store():
    try:
        # Obtén los datos de ubicación del dispositivo desde los parámetros de la solicitud GET
        data = request.get_json()
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        radio = data.get('radio')

        stores = Store.query.all()

        nearest_store = get_nearest_store(float(latitud), float(longitud), stores, float(radio))
        if nearest_store:
            return jsonify({
                'id': nearest_store[0].id,
                'name': nearest_store[0].name,
                'distance_km': nearest_store[1]
            })
        else:
            return jsonify({'error': 'No se encontró ninguna tienda cercana dentro del radio especificado.'}), 404
    except:
        return jsonify({"error": "Error al recibir los datos"})

"""
Este es un comentario que describe una ruta para obtener tiendas cercanas dentro de un radio.

URL: http://iaelchavez.pythonanywhere.com/get_nearby_stores
Método: GET
Respuesta: Objeto JSON con tiendas cercanas o un objeto JSON de error si no se encuentran tiendas dentro del radio especificado.
Ejemplo de uso: Accede a la ruta /get_nearby_stores con parámetros de latitud, longitud y radio.
"""
@app.route('/get_nearby_stores', methods=['GET'])
def get_nearby_stores():
    try:
        # Obtén los datos de ubicación del dispositivo desde los parámetros de la solicitud GET
        data = request.get_json()
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        radio = data.get('radio')

        stores = Store.query.all()
        nearby_stores = get_nearest_stores(float(latitud), float(longitud), stores)

        if nearby_stores:
            return jsonify(nearby_stores)
        else:
            return jsonify({'error': 'No se encontró ninguna tienda cercana dentro del radio especificado.'}), 404
    except:
        return jsonify({"error": "Error al recibir los datos"})

# Iniciar la aplicación si se ejecuta como script principal

if __name__ == "_main_":
    with app.app_context:
        db.create_all()

    app.run(debug=True)