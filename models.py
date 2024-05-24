from pydantic import BaseModel,Field
from datetime import datetime,date
from typing import Optional

class DetallePedido(BaseModel):
    idProducto:int
    cantidad:int
    precio:float
    subtotal:float
    costoEnvio:float
    subtotalEnvio:float

class PedidoInsert(BaseModel):
    idComprador:int
    idVendedor:int
    fechaRegistro:datetime=Field(default=datetime.now())
    costosEnvio:float=Field(...,ge=0)
    subtotal:float=Field(...,gt=0)
    total:float=Field(...,gt=0)
    estatus:str=Field(default='Captura')
    detalle:list[DetallePedido]

class Pago(BaseModel):
    fecha:datetime=Field(default=datetime.now())
    monto:float=Field(ge=0)
    idTarjeta:int
    estatus:str=Field(default='Aprobado')

class PedidoPay(BaseModel):
    estatus:str=Field(default='Pagado')
    pago:Pago

class PedidoCancelado(BaseModel):
    estatus:str=Field(default="Cancelado")
    motivoCancelacion:str

class DetallePedidoConsulta(BaseModel):
    idProducto:int
    cantidad:int
    precio:float
    subtotal:float
    costoEnvio:float
    subtotalEnvio:float
    nombreProducto:str

class PagoConsulta(BaseModel):
    fecha:datetime
    monto:float
    idTarjeta:int
    estatus:str
    noTarjeta:str
class Comprador(BaseModel):
    idComprador:int
    nombre:str
class Vendedor(BaseModel):
    idVendedor:int
    nombre:str

class Pedido(BaseModel):
    idPedido:str
    fechaRegistro:datetime
    fechaConfirmacion:datetime|None=None
    fechaCierre:datetime|None=None
    costosEnvio:float
    subtotal:float
    total:float
    estatus:str
    motivoCancelacion:str|None=None
    valoracion:int|None=None
    detalle:list[DetallePedidoConsulta]
    pago:PagoConsulta|None=None
    comprador:Comprador
    vendedor:Vendedor

class Respuesta(BaseModel):
    estatus:str
    mensaje:str

class PedidosConsulta(Respuesta):
    pedidos:list[Pedido]|None=None

class PedidoConsulta(Respuesta):
    pedido:Pedido|None=None

class Usuario(BaseModel):
    idUsuario:int=Field(alias="_id")
    nombre:str
    email:str
    password:str
    estatus:str
    telefono:str
    tipo:str
    domicilio:str
class UsuarioSalida(Respuesta):
    usuario:Usuario|None=None

