from flask_script import Manager,prompt_bool

from app import app,db

from modelo.models import Usuario
from getpass import getpass

manager = Manager(app)


@manager.command
def create_admin():
    usuario = {"nombreCompleto": input("Nombre:"),
               "email": input("Correo:"),
               "password":getpass("Password:"),
               "direccion":input("Direccion:"),
               "telefono":input("Telefono:"),
               "tipo":'A',
               "estatus":'A'}
    if prompt_bool("Are you sure you want save"):
        print("entro")
        usu = Usuario()
        usu.nombreCompleto = usuario["nombreCompleto"]
        usu.email = usuario["email"]
        usu.password = usuario["password"]
        usu.tipo = usuario["tipo"]
        usu.estatus = usuario["estatus"]
        db.session.add(usu)
        db.session.commit()
        print(usuario)
        quit(0)

if __name__ == '__main__':
    manager.run()