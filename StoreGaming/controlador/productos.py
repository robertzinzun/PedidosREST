import math

from flask import Blueprint,render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
import modelo


productos=Blueprint('productos',__name__)

@productos.route('/productos2')
def consultarProductos2():
    pdao = modelo.Dao.ProductoDAO()
    productos = pdao.consultaGeneral()
    renglones = math.ceil(len(productos) / 6)

    return render_template('productos/productos2.html', productos=productos,renglones=renglones)

@productos.route('/productos')
def consultarProductos():
    pdao= modelo.Dao.ProductoDAO()
    productos=pdao.consultaGeneral()
    return render_template('productos/productos.html',productos=productos)

@productos.route('/productos/foto/<int:id>')
def consultarFoto(id):
    pdao= modelo.Dao.ProductoDAO()
    foto=pdao.consultarFoto(id)
    return foto

@login_required
@productos.route('/productos/nuevo')
def nuevoProducto():
    cdao= modelo.Dao.CategoriaDAO()
    categorias=cdao.consultaGeneral()
    return render_template('productos/productoNuevo.html',categorias=categorias)

@login_required
@productos.route('/productos/insertar',methods=['POST'])
def guardarProducto():
    prod= modelo.models.Producto()
    prod.nombre=request.form['nombre']
    prod.descripcion=request.form['descripcion']
    prod.precio=request.form['precio']
    prod.existencia=request.form['existencia']
    prod.idCategoria=request.form['categoria']
    prod.foto=request.files['foto'].stream.read()
    prod.especificaciones=request.files['especificaciones'].stream.read()
    pdao = modelo.Dao.ProductoDAO()
    pdao.insertar(prod)
    return redirect(url_for('productos.consultarProductos'))

@login_required
@productos.route('/productos/eliminar/<int:id>')
def eliminarProducto(id):
    pdao = modelo.Dao.ProductoDAO()
    pdao.eliminar(id)
    return redirect(url_for('productos.consultarProductos'))

@login_required
@productos.route('/productos/<int:id>')
def consultarProducto(id=1):
    pdao = modelo.Dao.ProductoDAO()
    prod=pdao.consultaIndividual(id)
    cdao = modelo.Dao.CategoriaDAO()
    categorias = cdao.consultaGeneral()
    return render_template('productos/producto.html',producto=prod,categorias=categorias)

@productos.route('/productos/documento/<int:id>')
def consultarDocumento(id):
    pdao = modelo.Dao.ProductoDAO()
    doc = pdao.consultarDocumento(id)
    return doc

@productos.route('/productos/modificar',methods=['POST'])
def modificarProducto():
    prod = modelo.models.Producto()
    prod.idProducto =request.form['id']
    prod.nombre = request.form['nombre']
    prod.descripcion = request.form['descripcion']
    prod.precio = request.form['precio']
    prod.existencia = request.form['existencia']
    prod.idCategoria = request.form['categoria']
    foto=request.files['foto'].stream.read()
    doc=request.files['especificaciones'].stream.read()
    if foto:
        prod.foto=foto
    if doc:
        prod.especificaciones=doc
    pdao = modelo.Dao.ProductoDAO()
    pdao.modificar(prod)
    return redirect(url_for('productos.consultarProductos'))
