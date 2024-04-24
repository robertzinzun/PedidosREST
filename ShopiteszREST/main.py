from flask import Flask,request
from modelo.DAO import db,Producto,Pedido,DetallePedido,Usuario,Tarjeta
from flask_httpauth import HTTPBasicAuth
from BPProductos import productosBP #Importar BP
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userShopiteszSOA:Shopitesz.123@localhost/ShopiteszSOA'
app.register_blueprint(productosBP)#registrar BP
auth=HTTPBasicAuth()
@auth.verify_password
def validarUsuario(email,password):
    usuario=Usuario()
    user=usuario.autenticar(email,password)
    if user:
        return user
    else:
        return False
@auth.get_user_roles
def get_user_roles(user):
    return user.tipo

@auth.error_handler
def error_handler():
    return {"estatus":"Error","mensaje":"Sin autorizacion"}
@app.route('/')
def inicio():
    return {"estatus":"OK","mensaje":"Escuchando ServiciosREST"}
@app.route('/pedidos',methods=['Post'])
@auth.login_required(role='Comprador')
def agregarPedido():
    datosPedidos=request.get_json()
    pedido=Pedido()
    return pedido.agregar(datosPedidos)
@app.route('/pedidos',methods=['Get'])
@auth.login_required(role=['Administrador','Comprador','Vendedor'])
def consultarPedidos():
    pedido=Pedido()
    return pedido.consultaGeneral()
@app.route('/pedidos',methods=['Put'])
@auth.login_required(role=['Comprador','Vendedor'])
def modificarPedido():
    datosPedidos=request.get_json()
    pedido=Pedido()
    #REvisar si ya esta pagando el pedido lanzar la ejecucion del transferencia
    return pedido.modificar(datosPedidos)
@app.route('/pedidos/agregarProducto',methods=['put'])
@auth.login_required(role=['Comprador'])
def agregarProductoPedido():
    datos=request.get_json()
    detallePedido=DetallePedido()
    return detallePedido.agregar(datos)
@app.route('/pedidos/modificarProducto',methods=['Put'])
def modificarProductoPedido():
    datos=request.get_json()
    detallePedido=DetallePedido()
    return detallePedido.modificar(datos)
@app.route('/pedidos/<int:idPedido>',methods=['Get'])
@auth.login_required(role=['Administrador','Comprador','Vendedor'])
def consultarPedido(idPedido):
    pedido=Pedido()
    return pedido.consultaIndividual(idPedido)
@app.route('/pedidos/eliminarProducto',methods=['Delete'])
def eliminarProductoPedido():
    datos=request.get_json()
    detallePedido=DetallePedido()
    return detallePedido.eliminar(datos)
@app.route('/pedidos/<int:idPedido>',methods=['Delete'])
@auth.login_required(role='Comprador')
def eliminarPedido(idPedido):
    pedido=Pedido()
    return pedido.cancelar(idPedido)
@app.route('/pedidos/detalle',methods=['Get'])
def consultarDetalle():
    datos=request.get_json()
    detalle=DetallePedido()
    return detalle.consultarDetalle(datos['idPedido'],datos['idProducto'])
@app.route('/pedidos/comprador/<int:idComprador>',methods=['Get'])
@auth.login_required(role=['Comprador'])
def consultarPedidosComprador(idComprador):
    pedido=Pedido()
    return pedido.consultarPorComprador(idComprador)
@app.route('/pedidos/vendedor/<int:idVendedor>',methods=['Get'])
@auth.login_required(role=['Vendedor'])
def consultarPedidosVendedor(idVendedor):
    pedido=Pedido()
    return pedido.consultarPorVendedor(idVendedor)
# Press the green button in the gutter to run the script.
@app.route('/usuarios/autenticar',methods=['Get'])
def autenticar():
    usuario=Usuario()
    datos=request.get_json()
    user=usuario.autenticar(datos["email"],datos["password"])
    respuesta={"estatus":"","mensaje":""}
    if user:
        respuesta["estatus"]="OK"
        respuesta["mensaje"]="Usuario encontrado"
        respuesta["usuario"]=user.to_json()
    else:
        respuesta["estatus"]="Error"
        respuesta["mensaje"]="El usuario no existe o password incorrecto"
    return respuesta
@app.route('/usuarios/<int:idUsuario>',methods=['Get'])
def consultarUsuario(idUsuario):
    usuario=Usuario()
    return usuario.consultaIndividual(idUsuario)
@app.route('/tarjetas/usuario/<int:idUsuario>',methods=['Get'])
def consultarPorUsuario(idUsuario):
    tarjeta=Tarjeta()
    return tarjeta.consultaPorUsuario(idUsuario)
if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True,host="0.0.0.0",port="5001")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
