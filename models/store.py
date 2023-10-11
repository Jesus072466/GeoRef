class Store(object):
    IDStore = "sumary_line"
    name = ""
    latitude = "d"
    longitude = "l"

    def get_IDStore(self):
        return self.IDStore

    def set_IDStore(self, IDStore):
        self.IDStore = IDStore

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_latitud(self):
        return self.latitud

    def set_latitud(self, latitud):
        self.latitud = latitud

    def get_longitud(self):
        return self.longitud

    def set_longitud(self, longitud):
        self.longitud = longitud