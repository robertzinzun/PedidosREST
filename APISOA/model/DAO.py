import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String,text,Date,Float
db=SQLAlchemy()
class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=db.Column(Integer,primary_key=True)
    nombre=db.Column(String,unique=True)

    def consultar(self):
        respuesta={"categorias":""}
        lista=self.query.all()
        respuesta["categorias"]=[c.to_json() for c in lista ]
        print(lista)
        return respuesta

    def to_json(self):
        categoria={"id":self.idCategoria,"nombre":self.nombre}
        return categoria
class Producto(db.Model):
    __tablename__='vProductos'
    idProducto=db.Column(Integer,primary_key=True)
    nombre=db.Column(String)

    def consultar(self):
        respuesta={"productos":""}
        lista=self.query.all()
        respuesta['productos']=[p.to_json() for p in lista]
        return respuesta
    def view(self):
        db.session.execute(text('call sp_agregar_pedido(1,1,6,@pestatus,@pmensaje)'))
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        print(salida[0],' ',salida[1])
        db.session.commit()
    def to_json(self):
        producto={"id":self.idProducto,"nombre":self.nombre}
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
        db.session.execute(text('call sp_agregar_pedido(:idComprador,:idVendedor,'
                                ':idTarjeta,@pestatus,@pmensaje)'),parametros)
        db.session.commit()
        salida=db.session.execute(text('select @pestatus,@pmensaje')).fetchone()
        respuesta={"esatus":salida[0],"mensaje":salida[1]}
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
    def consultaIndividual(self,idPedido):
        respuesta={"estatus":"","mensaje":"","pedido":""}
        pedido=self.query.get(idPedido)
        if pedido:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="Listado del pedido con Id:"+str(idPedido)
            respuesta["pedido"]=pedido.to_json()
            dp=DetallePedido()
            respuesta.get("pedido")["productos"]=dp.consultaPorPedido(idPedido)
        else:
            respuesta["estatus"]="OK"
            respuesta["mensaje"]="El pedido con Id:"+str(idPedido)+" no existe."
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

    def consultaGeneral(self):
        lista=self.query.all()
        for dp in lista:
            print(dp.nombre)
    def consultaPorPedido(self,idPedido):
        listaProductos=[]
        lista=self.query.filter(DetallePedido.idPedido==idPedido).all()
        if len(lista)>0:
            for dp in lista:
                listaProductos.append(dp.to_json())
        return listaProductos

    def to_json(self):
        detalle={
            "idProducto":self.idProducto,
            "nombre":self.nombre,
            "cantidad":self.cantidad,
            "precio":self.precio,
            "costoEnvio":self.costoEnvio,
            "subtotal":self.subtotal,
            "subtotalEnvio":self.subtotalEnvio
        }
        return detalle