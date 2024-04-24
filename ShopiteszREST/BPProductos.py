from flask import Blueprint
from modelo.DAO import Producto
productosBP=Blueprint('ProductosBP',__name__)

@productosBP.route('/productos',methods=['Get'])
def consultarProductos():
    producto=Producto()
    return producto.consultaGeneral()
@productosBP.route('/productos/<int:idProducto>',methods=['Get'])
def consultarProducto(idProducto):
    producto=Producto()
    return producto.consultaIndividual(idProducto)

@productosBP.route('/productos/imagen/<int:id>',methods=['Get'])
def consultarImagenProducto(id):
    p=Producto()
    return p.consultarFoto(id)
@productosBP.route('/productos/vendedor/<int:idVendedor>',methods=['Get'])
def consultarProductosPorVendedor(idVendedor):
    p=Producto()
    return p.consultarPorVendedor(idVendedor)