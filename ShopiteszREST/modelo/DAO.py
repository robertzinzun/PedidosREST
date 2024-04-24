from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,Float,text,Date,BLOB
db=SQLAlchemy()
#Crear una clase de Python para vincular la clase con una tabla de la BD
class Producto(db.Model):
    __tablename__='vProductos'
    idProducto=db.Column(Integer,primary_key=True)
    nombre=db.Column(String)
    descripcion=db.Column(String)
    precio=db.Column(Float)
    costoEnvio=db.Column(Float)
    existencia=db.Column(Integer)
    color=db.Column(String)
    marca=db.Column(String)
    estatus=db.Column(String)
    idCategoria=db.Column(Integer)
    nombre_categoria=db.Column(String)
    idVendedor=db.Column(Integer)
    nombre_vendedor=db.Column(String)
    foto=db.Column(BLOB)
    #Metodo de la clase que realizar una consulta de tipo select a la vista vProductos
    def consultaGeneral(self):
        respuesta={"estatus":"","mensaje":"","productos":[]}
        lista=self.query.all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado general de productos"
            respuesta["productos"]=[prod.to_json() for prod in lista]
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="No existen productos registrados"
        return respuesta
    def consultarFoto(self,idProducto):
        prod=self.query.get(idProducto)
        return prod.foto

    def consultaIndividual(self,idProducto):
        respuesta={"estatus":"","mensaje":"","producto":""}
        producto=self.query.get(idProducto)
        if producto!=None:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado del producto con Id: "+str(idProducto)
            respuesta["producto"]=producto.to_json()
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="El producto con Id: "+str(idProducto)+" no existe"
        return respuesta
    def consultarPorVendedor(self,idVendedor):
        respuesta={"estatus":"","mensaje":"","productos":[]}
        lista=self.query.filter(Producto.idVendedor==idVendedor).all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado general de productos"
            respuesta["productos"]=[prod.to_json() for prod in lista]
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="No existen productos registrados"
        return respuesta
    def to_json(self):
        producto={
            "idProducto":self.idProducto,
            "nombre":self.nombre,
            "descripcion": self.descripcion,
            "precio" : self.precio,
            "costoEnvio" : self.costoEnvio,
            "existencia" : self.existencia,
            "color" : self.color,
            "marca" : self.marca,
            "estatus" :self.estatus,
            "categoria":{"idCategoria":self.idCategoria,"nombre":self.nombre_categoria},
            "vendedor":{"idVendedor":self.idVendedor,"nombre":self.nombre_vendedor}
        }
        return producto
class Pedido(db.Model):
    __tablename__='vPedidos'
    idPedido=db.Column(Integer,primary_key=True)
    idComprador=db.Column(Integer)
    idVendedor=db.Column(Integer)
    idTarjeta=db.Column(Integer)
    fechaRegistro=db.Column(Date)
    fechaAtencion=db.Column(Date)
    fechaCierre=db.Column(Date)
    costesEnvio=db.Column(Float)
    subtotal=db.Column(Float)
    totalPagar=db.Column(Float)
    valoracion=db.Column(Integer)
    estatus=db.Column(String)
    idTarjeta=db.Column(Integer)
    noTarjeta=db.Column(String)
    idComprador=db.Column(Integer)
    comprador=db.Column(String)
    idVendedor=db.Column(Integer)
    vendedor=db.Column(String)

    def agregar(self,parametros):
        db.session.execute(text('call sp_agregar_pedido(:idComprador,:idVendedor,:idTarjeta,:idProducto,:cantidad,@pestatus,@pmensaje)'),parametros)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        print(salida[0])
        respuesta={"estatus":salida[0],"mensaje":salida[1]}
        return respuesta
    def modificar(self,parametros):
        db.session.execute(text('call sp_modificar_pedido(:idPedido,:idTarjeta,:valoracion,:estatus,:tipoUsuario,@pestatus,@pmensaje)'),parametros)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        print(salida[0])
        respuesta={"estatus":salida[0],"mensaje":salida[1]}
        return respuesta
    def consultaGeneral(self):
        respuesta={"estatus":"","mensaje":"","pedidos":[]}
        lista=self.query.all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado general de pedidos"
            respuesta["pedidos"]=[ped.to_json() for ped in lista]
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="No existen pedidos registrados"
        return respuesta
    def to_json(self):
        pedido={
            "idPedido":self.idPedido,
            "fechaRegistro": self.fechaRegistro.isoformat() ,
            "fechaAtencion":self.fechaAtencion if self.fechaAtencion==None else self.fechaAtencion.isoformat(),
            "fechaCierre":self.fechaCierre if self.fechaCierre==None else self.fechaCierre.isoformat(),
            "costosEnvio":self.costesEnvio,
            "subtotal":self.subtotal,
            "totalPagar":self.totalPagar,
            "valoracion":self.valoracion,
            "estatus":self.estatus,
            "tarjeta":{"idTarjeta":self.idTarjeta,"noTarjeta":self.noTarjeta},
            "comprador":{"idComprador":self.idComprador,"nombre":self.comprador},
            "vendedor":{"idVendedor":self.idVendedor,"nombre":self.vendedor}
        }
        return pedido
    def consultaIndividual(self,idPedido):
        respuesta={"estatus":"","mensaje":"","pedido":""}
        pedido=self.query.get(idPedido)
        if pedido:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado del pedido con Id:"+str(idPedido)
            respuesta["pedido"]=pedido.to_json()
            detallePedido=DetallePedido()
            respuesta.get("pedido")["productos"]=detallePedido.consultarDetallePedido(idPedido)
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="El pedido con Id:"+str(idPedido)+" no existe."
        return respuesta
    def consultarPorComprador(self,idComprador):
        respuesta={"estatus":"","mensaje":"","pedidos":""}
        lista=self.query.filter(Pedido.idComprador==idComprador).all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado de pedidos"
            respuesta["pedidos"]=[pedido.to_json() for pedido in lista]
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="El usuario no tiene pedidos registrados"
        return respuesta
    def consultarPorVendedor(self,idVendedor):
        respuesta={"estatus":"","mensaje":"","pedidos":""}
        lista=self.query.filter(Pedido.idVendedor==idVendedor).all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado de pedidos"
            respuesta["pedidos"]=[pedido.to_json() for pedido in lista]
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="El usuario no tiene pedidos registrados"
        return respuesta
    def cancelar(self,idPedido):
        parametros={"idPedido":idPedido}
        respuesta={"estatus":"","mensaje":""}
        db.session.execute(text('call sp_eliminar_pedido(:idPedido,@pestatus,@pmensaje)'),parametros)
        db.session.commit()
        salida=db.session.execute(text("select @pestatus,@pmensaje")).fetchone()
        respuesta["estatus"]=salida[0]
        respuesta["mensaje"]=salida[1]
        return respuesta

class DetallePedido(db.Model):
    __tablename__='vDetallePedido'
    idPedido=db.Column(Integer,primary_key=True)
    idProducto=db.Column(Integer,primary_key=True)
    nombre=db.Column(String)
    cantidad=db.Column(Integer)
    precio=db.Column(Float)
    costoEnvio=db.Column(Float)
    subtotal=db.Column(Float)
    subtotalEnvio=db.Column(Float)
    #Operación para agregar un producto al pedido
    def agregar(self,detalle):

        db.session.execute(text('call sp_agregar_producto_pedido(:idPedido,:idProducto,:cantidad,@pestatus,@pmensaje)'),detalle)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        respuesta={"estatus":salida[0],"mensaje":salida[1]}
        print(respuesta)
        return respuesta
    def modificar(self,detalle):
        respuesta={"estatus":"","mensaje":""}
        db.session.execute(text('call sp_actualizar_producto_pedido(:idPedido,:idProducto,:cantidad,@pestatus,@pmensaje)'),detalle)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        respuesta["estatus"]=salida[0]
        respuesta["mensaje"]=salida[1]
        return respuesta
    def consultarDetallePedido(self,idPedido):
        lista=self.query.filter(DetallePedido.idPedido==idPedido).all()
        listaJson=[]
        if len(lista)>0:
            for dp in lista:
                listaJson.append(dp.to_json())
        return listaJson
    def consultarDetalle(self,idPedido,idProducto):
        detalle=self.query.filter(DetallePedido.idPedido==idPedido,DetallePedido.idProducto==idProducto).first()
        respuesta={"estatus":"","mensaje":"","detalle":""}
        if detalle:
            respuesta["estatus"]='OK'
            respuesta["mensaje"]="Listado del producto del pedido"
            respuesta["detalle"]=detalle.to_json()
        else:
            respuesta["estatus"]='Error'
            respuesta["mensaje"]="El producto no existe en el pedido"
        return respuesta

    def to_json(self):
        detalle={
            "idPedido":self.idPedido,
            "idProducto":self.idProducto,
            "nombre":self.nombre,
            "precio":self.precio,
            "cantidad":self.cantidad,
            "costoEnvio":self.costoEnvio,
            "subtotal":self.subtotal,
            "subtotalEnvio":self.subtotalEnvio
        }
        return detalle
    def eliminar(self,parametros):
        respuesta={"estatus":"","mensaje":""}
        db.session.execute(text('call sp_eliminar_producto_pedido(:idPedido,:idProducto,@pestatus,@pmensaje)'),parametros)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        respuesta["estatus"]=salida[0]
        respuesta["mensaje"]=salida[1]
        return respuesta
class Usuario(db.Model):
    __tablename__='Usuarios'
    idUsuario=db.Column(Integer,primary_key=True)
    nombre=db.Column(String)
    email=db.Column(String,unique=True)
    password=db.Column(String)
    tipo=db.Column(String)
    estatus=db.Column(String)
    def autenticar(self,email,password):
        user=self.query.filter(Usuario.email==email,
        Usuario.password==password,Usuario.estatus=='A').first()
        return user
    def to_json(self):
        usuario={'idUsuario':self.idUsuario,
                 "nombre":self.nombre,
                 "email":self.email,
                 "password":self.password,
                 "tipo":self.tipo,
                 "estatus":self.estatus}
        return usuario
    def consultaIndividual(self,idUsuario):
        user=self.query.get(idUsuario)
        respuesta={"estatus":"","mensaje":"","usuario":""}
        if user:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado del usuario"
            respuesta["usuario"]=user.to_json()
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="El usuario no existe"
        return respuesta
class Tarjeta(db.Model):
    __tablename__='Tarjetas'
    idTarjeta=db.Column(Integer,primary_key=True)
    idUsuario=db.Column(Integer)
    noTarjeta=db.Column(String)
    emisor=db.Column(String)
    cvc=db.Column(String)
    anioVigencia=db.Column(Integer)
    mesVigencia=db.Column(Integer)
    tipo=db.Column(String)
    estatus=db.Column(String)

    def consultaPorUsuario(self,idUsuario):
        respuesta={"estatus":"","mensaje":"","tarjetas":""}
        lista=self.query.filter(Tarjeta.idUsuario==idUsuario,Tarjeta.estatus=='A').all()
        if len(lista)>0:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado de Tarjetas por Usuario"
            respuesta["tarjetas"]=[t.to_json() for t in lista]
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="El usuario no tiene tarjetas registradas"
        return respuesta
    def to_json(self):
        tarjeta={
            "idTarjeta":self.idTarjeta,
            "idUsuario":self.idUsuario,
            "noTarjeta":self.noTarjeta,
            "emisor":self.emisor,
            "cvc":self.cvc,
            "vigencia":str(self.mesVigencia)+"/"+str(self.anioVigencia),
            "tipo":self.tipo,
            "estatus":self.estatus
        }
        return tarjeta
