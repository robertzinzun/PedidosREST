import sqlalchemy.orm
from  flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Binary,ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import gen_salt, generate_password_hash,check_password_hash

from app import db

class Usuario(UserMixin, db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String(60),nullable=False)
    email=Column(String(60),nullable=False)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)
    direccion=Column(String(100),nullable=False)
    telefono=Column(String(12),nullable=False)

    def __repr__(self):
        return self.nombreCompleto

    @property
    def password(self):
        raise AttributeError('El password no es un atributo de lectura')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.idUsuario)

    def is_admin(self):
        if(self.tipo=='A'):
            return True
        else:
            return False

class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String(50),nullable=False)


    def __repr__(self):
        return self.nombre

class Producto(db.Model):
    __tablename__='productos'
    idProducto=Column(Integer,primary_key=True)
    nombre=Column(String(50),nullable=False)
    descripcion=Column(String(100))
    precio=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(Binary)
    especificaciones=Column(Binary)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    categoria=relationship(Categoria,backref='Categoria.idCategoria',lazy='select')
