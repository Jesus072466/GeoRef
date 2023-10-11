"""
:author: José María Cruz Parada
:type: POST
:param: El cliente debe enviar un JSON que contiene el 'id' de la tienda
        de referencia.
:return: Una respuesta JSON con la lista de productos ordenados según
         tiendas cercanas a la tienda de referencia.
:descrip: Endpoint para obtener productos basados en la proximidad de las
          tiendas.
"""
@app.route('/get_products_store',methods=['POST'])
def get_products_store():
    # Obtener el id del Body de la petición
    data = request.get_json()
    id_store = data.get('id')

    # Consultar tiendas cercanas basadas en el 'id' proporcionado
    stores = nearby_stores_by_store(id_store)

    # Obtener productos de esas tiendas cercanas y ordenarlos según
    # la proximidad de las tiendas
    products = get_products_by_store_ids(stores)

    # Retornar los productos como una respuesta JSON
    return jsonify(products)

    """
:author: José María Cruz Parada
:param: ID de la tienda de referencia
:return: Lista de las tiendas ordenadas por la distancia entre la tienda de
         referencia y las demás
:descrip: Consultas las tiendas más cercanas respecto a una tienda
"""
def nearby_stores_by_store(id_store):
    # Extraer los ids de las tiendas cercanas ordenadas por distancia
    nearby_stores = db.session.query(
        DistanceStore.idReference2
    ).filter(
        DistanceStore.idReference == id_store
    ).order_by(
        DistanceStore.distance
    ).all()

    # id tienda de referencia + ids tiendas más cernas ordenadas por distancia
    stores = [id_store] + [
        store[0]
        for store in nearby_stores
    ]

    return stores


"""
:author: José María Cruz Parada
:param: Lista de ids de tiendas ordenada por distancia
:return: Lista de productos de los más cercanos al más lejano respcto a la
         distancia entre tiendas
:descrip: Obtener los productos respecto a las distancia entre tiendas
"""
def get_products_by_store_ids(stores):
    # Crear un mapeo ordenado para los stores
    order_by_clause = case(
        *((ProductDetail.idStore == store, index) for index, store in enumerate(stores)),
    ).asc()

    # Consulta para obtener los productos de las tiendas en el orden especificado
    products_ordered = db.session.query(
        ProductDetail,
        Product.name,
        Product.description
    ).join(
        Product, ProductDetail.idProduct == Product.idProduct
    ).filter(
        ProductDetail.idStore.in_(stores)
    ).order_by(
        order_by_clause
    ).all()

    # Convertir los productos en una lista de diccionarios
    products = [
        {
            "idProduct": product[0].idProduct,
            "idStore": product[0].idStore,
            "price": product[0].price,
            "stock": product[0].stock,
            "name": product[1],
            "description": product[2]
        }
        for product in products_ordered
    ]

    return products