from modelo.models import Categoria, Producto
from modelo.models import Usuario
from flask_mail import Message
from flask import render_template
from threading import Thread

from app import db, app
from app import mail
class CategoriaDAO:
    def consultaGeneral(self):
        try:
            categorias=Categoria.query.all()
        except:
            categorias=[]
        return categorias
    def consultaIndividual(self,id):
        try:
            categoria=Categoria.query.filter_by(idCategoria=id).first()
        except:
            categoria=None
        return categoria
    def insertar(self,Categoria):
        try:
            db.session.add(Categoria)
            db.session.commit()
        except:
            print('Error: al insertar la catergoria')
    def modificar(self,categoria):
        try:
            db.session.merge(categoria)
            db.session.commit()
        except:
            print('Error al modificar la categoria')
    def eliminar(self,id):
        try:
            categoria=self.consultaIndividual(id)
            db.session.delete(categoria)
            db.session.commit()
        except:
            print('Error al eliminar la categoria')

class UsuarioDAO:
    def consultarPorEmail(self,email):
        try:
            user = Usuario.query.filter_by(email=email).first()
        except:
            user=None
        return user
    def validar(self,email,password):
        user=Usuario.query.filter_by(email=email,estatus='A').first()
        if user!=None and user.validarPassword(password):
            return user
        else:
            return None
    def registrar(self,usuario):
        try:
            db.session.add(usuario)
            db.session.commit()
        except:
            print('Error al agregar al usuario')
    def existeCorreo(self,correo):
        if Usuario.query.filter_by(email=correo).first():
            return True
        else:
            return False
    def modificar(self,usuario):
        try:
            db.session.merge(usuario)
            db.session.commit()
        except:
            print('Error al modificar al usuario')
    def consultaGeneral(self,id):
        try:
            usuarios=Usuario.query.filter(Usuario.idUsuario!=id).all()
        except:
            usuarios=[]
        return usuarios
    def consultaIndividual(self,id):
        try:
            usuario=Usuario.query.get(int(id))
        except:
            usuario=None
        return usuario
    def eliminar(self,id):
        try:
            usuario=self.consultaIndividual(id)
            usuario.estatus='B'
            self.modificar(usuario)
        except:
            print('Error al eliminar el usuario')

class ProductoDAO:
    def consultaGeneral(self):
        try:
            productos=Producto.query.all()
        except:
            productos=[]
        return productos
    def consultarFoto(self,id):
        try:
            prod=Producto.query.get(id)
            foto=prod.foto
        except:
            foto=None
        return foto
    def insertar(self,producto):
        try:
            db.session.add(producto)
            db.session.commit()
        except:
            print('Error al agregar el producto')
    def consultaIndividual(self,id):
        try:
            producto=Producto.query.get(id)
        except:
            producto=None
        return producto
    def eliminar(self,id):
        try:
            producto=self.consultaIndividual(id)
            db.session.delete(producto)
            db.session.commit()
        except:
            print('Error al eliminar el producto')
    def consultarDocumento(self,id):
        try:
            prod = Producto.query.get(id)
            doc=prod.especificaciones
        except:
            doc=None
        return doc
    def modificar(self,producto):
        try:
            db.session.merge(producto)
            db.session.commit()
        except:
            db.session.rollback()

class MailSender:
    def enviarEmail(self,asunto,template,user):
        try:
            msg=Message(asunto,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[user.email])
            msg.html=render_template(template+'.html',user=user)
            hilo=Thread(target=self.send_async_email,args=[app,msg])
            hilo.start()
            return hilo
        except:
            print('Error al enviar el correo')
    def send_async_email(self,app,msg):
        with app.app_context():
            mail.send(msg)