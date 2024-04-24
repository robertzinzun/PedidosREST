import requests
from flask_login import UserMixin

class Opcion:
    url='http://172.16.1.135:8000/opciones'
    def consultaGeneral(self):
        respuesta=requests.get(self.url)
        print(respuesta.json())
        return respuesta.json()

class Usuario(UserMixin):
    id=0
    nombre=None
    email=None
    telefono=None
    tipo=None
    activo=False
    def is_authenticated(self):
        return True;
    def is_active(self):
        return self.activo
    def is_anonymous(self):
        return False
    def get_id(self):
        return  self.id