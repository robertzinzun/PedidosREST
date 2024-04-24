import requests
from threading import Event,Timer
from flask import Flask,render_template,request,session,redirect,url_for,g
from flask_bootstrap import Bootstrap
import json
import  requests
from requests.auth import HTTPBasicAuth
from suds.client import Client
app=Flask(__name__)
app.secret_key='Cl4v3'
bootstrap=Bootstrap(app)
urlServicio='http://127.0.0.1:5001/'
urlWSDL='http://localhost:8090/BancoSOA/TransferenciaService?WSDL'
@app.route('/')
def inicio():
    return render_template('comunes/index.html')
@app.route('/productos')
def productos():
    url=urlServicio+'productos'
    respuesta=requests.get(url).json()
    lista=[]
    if respuesta["estatus"]=="OK" and len(respuesta["productos"])>0:
        lista=respuesta["productos"]
    return render_template('productos/listar.html',productos=lista)
@app.route('/productos/imagen/<int:id>')
def consultarImagen(id):
    url=urlServicio+'productos/imagen/'+str(id)
    return requests.get(url).content
@app.route('/login',methods=['Post'])
def login():

    usuario={"email":request.form['email'],
             "password":request.form['password']}
    url=urlServicio+'usuarios/autenticar'
    respuesta=requests.get(url,json=usuario).json()
    if(respuesta["estatus"]=='OK'):
        session['usuario']=respuesta['usuario']
        return render_template('comunes/principal.html')
    else:
        return render_template('comunes/index.html')

@app.before_request
def obtenerCredenciales():
    if 'usuario' in session:
        user=session.get('usuario')
        g.user=user
        g.credenciales=HTTPBasicAuth(user['email'], user['password'])

@app.route('/usuarios/cerrarSesion')
def cerrarSesion():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route('/pedidos/nuevo/<int:idProducto>/<int:cantidad>',methods=['Get'])
def nuevoPedido(idProducto,cantidad):
    url=urlServicio+'productos/'+str(idProducto)
    respuesta=requests.get(url).json()
    producto=respuesta['producto']
    urlVendedor=urlServicio+'/usuarios/'+str(producto.get('vendedor')['idVendedor'])
    respuesta=requests.get(urlVendedor).json()
    vendedor=respuesta['usuario']
    urlTarjetas=urlServicio+'tarjetas/usuario/'+str(session.get('usuario')['idUsuario'])
    respuesta=requests.get(urlTarjetas).json()
    tarjetas=respuesta['tarjetas']
    detalle={"cantidad":cantidad,"subtotal":cantidad*producto['precio'],"subtotalEnvio":cantidad*producto['costoEnvio']}
    return render_template("pedidos/nuevo.html",producto=producto,tarjetas=tarjetas,vendedor=vendedor,detalle=detalle)
@app.route('/pedidos/agregar',methods=['Post'])
def agregarPedido():
    url1=urlServicio+'pedidos'
    datosPedido={
        "idComprador":int(session.get('usuario')['idUsuario']),
        "idVendedor":int(request.form['idVendedor']),
        "idTarjeta":int(request.form['idTarjeta']),
        "idProducto":int(request.form['idProducto']),
        "cantidad":int(request.form['cantidad'])
    }
    #credenciales= HTTPBasicAuth(session.get('usuario')['email'], session.get('usuario')['password'])
    print(url1)
    print(datosPedido)
    try:
        respuesta=requests.post(url1,json=datosPedido,auth=g.credenciales,timeout=10)
        print(respuesta.text)
    except Exception as ex:
        print(ex)
    return redirect(url_for('consultarPedidos'))
@app.route('/pedidos',methods=['Get'])
def consultarPedidos():
    pedidos=[]
    if g.user['tipo']=='Comprador':
        url=urlServicio+'pedidos/comprador/'+str(g.user['idUsuario'])
        respuesta=requests.get(url,auth=g.credenciales).json()
        pedidos=respuesta['pedidos']
    else:
        if g.user['tipo']=='Vendedor':
            url=urlServicio+'pedidos/vendedor/'+str(g.user['idUsuario'])
            respuesta=requests.get(url,auth=g.credenciales).json()
            pedidos=respuesta['pedidos']
        else:
            url=urlServicio+'pedidos'
            respuesta=requests.get(url,auth=g.credenciales).json()
            pedidos=respuesta['pedidos']
    return render_template('pedidos/listar.html',pedidos=pedidos)
@app.route('/pedidos/ver/<int:idPedido>',methods=['Get'])
def consultarPedido(idPedido):
    url=urlServicio+'pedidos/'+str(idPedido)
    respuesta=requests.get(url,auth=g.credenciales).json()
    if respuesta["estatus"]=='OK':
        pedido=respuesta['pedido']
        return render_template('pedidos/listadoIndividual.html',pedido=pedido)
@app.route('/pedidos/cancelar/<int:idPedido>',methods=['Get'])
def cancelarPedido(idPedido):
    url=urlServicio+'pedidos/'+str(idPedido)
    respuesta=requests.delete(url,auth=g.credenciales).json()
    return redirect(url_for('consultarPedido',idPedido=idPedido))
@app.route('/pedidos/nuevoProducto/<int:idPedido>/<int:idVendedor>',methods=['Get'])
def nuevoProducto(idPedido,idVendedor):
    url=urlServicio+'pedidos/'+str(idPedido)
    respuesta=requests.get(url,auth=g.credenciales).json()
    if respuesta["estatus"]=='OK':
        pedido=respuesta['pedido']
    url=urlServicio+'productos/vendedor/'+str(idVendedor)
    respuesta=requests.get(url,auth=g.credenciales).json()
    if respuesta["estatus"]=='OK':
        productos=respuesta['productos']
    return render_template('pedidos/agregarProducto.html',productos=productos,pedido=pedido)
@app.route('/pedidos/agregarProducto',methods=['Post'])
def agregarProducto():
    detalle={
        "idPedido":int(request.form["idPedido"]),
        "idProducto":int(request.form["idProducto"]),
        "cantidad":int(request.form["cantidadP"])
    }
    url=urlServicio+'pedidos/agregarProducto'
    respuesta=requests.put(url,json=detalle,auth=g.credenciales).json()
    return redirect(url_for('consultarPedido',idPedido=detalle['idPedido']))
@app.route('/pedidos/detalle/<int:idPedido>/<int:idProducto>',methods=['Get'])
def consultarDetalle(idPedido,idProducto):
    url=urlServicio+'pedidos/detalle'
    datos={"idPedido":idPedido,"idProducto":idProducto}
    respuesta=requests.get(url,json=datos,auth=g.credenciales).json()
    detalle=respuesta['detalle']
    return render_template('pedidos/editarProducto.html',detalle=detalle)
@app.route('/pedidos/detalle/eliminar/<int:idPedido>/<int:idProducto>',methods=['Get'])
def eliminarDetalle(idPedido,idProducto):
    datos={"idPedido":idPedido,"idProducto":idProducto}
    url=urlServicio+'/pedidos/eliminarProducto'
    respuesta=requests.delete(url,json=datos,auth=g.credenciales).json()
    return redirect(url_for('consultarPedido',idPedido=idPedido))
@app.route('/pedido/detalle/modificar',methods=['Post'])
def modificarDetalle():
    detalle={
        "idPedido":int(request.form["idPedido"]),
        "idProducto":int(request.form["idProducto"]),
        "cantidad":int(request.form["cantidad"])
    }
    url=urlServicio+'pedidos/modificarProducto'
    respuesta=requests.put(url,json=detalle,auth=g.credenciales).json()
    return redirect(url_for('consultarPedido',idPedido=detalle['idPedido']))
@app.route('/pedidos/modificar',methods=['Post'])
def modificarPedido():
    datos=request.get_json()
    cliente=Client(urlWSDL)

    if datos['estatus']=='Pagado':#Realizar transferencia
        url=urlServicio+'pedidos/'+datos['idPedido']
        respuesta=requests.get(url,auth=g.credenciales).json()
        pedido=respuesta['pedido']
        tarjetaOrigen=pedido.get('tarjeta')['noTarjeta']
        url=urlServicio+'tarjetas/usuario/'+str(pedido.get('vendedor')['idVendedor'])
        respuesta=requests.get(url).json()
        tarjetas=respuesta['tarjetas']
        for t in tarjetas:
            tarjetaDestino=t['noTarjeta']
        print("Tarjeta Origen:"+tarjetaOrigen)
        print("Tarjeta destino:"+tarjetaDestino)
        respuesta=cliente.service.transferir(tarjetaOrigen,tarjetaDestino,pedido['totalPagar'],'Pago del Pedido:'+str(pedido['idPedido']))
        print(respuesta)


    url=urlServicio+'pedidos'
    datos["tipoUsuario"]=g.user['tipo']
    respuesta=requests.put(url,json=datos,auth=g.credenciales).json()
    return respuesta

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
