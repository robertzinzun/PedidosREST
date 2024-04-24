from pydantic import BaseModel,Field
from typing import List
from datetime import date

class Categoria(BaseModel):
    id:int=Field(...,alias="_id")
    nombre:str
    estatus:str

class CategoriasCol(BaseModel):
    categorias:List[Categoria]

class Producto(BaseModel):
    id:str
    nombre:str
    categoria:Categoria

class Usuario(BaseModel):
    id:int=Field(...,alias="_id")
    email:str
    nombre:str
    tipo:str
class DetallePedido(BaseModel):
    idProducto:int
    cantidad:int
    precio:float
    subtotal:float
    costoEnvio:float
    subtotalEnvio:float

class PedidoInsert(BaseModel):
    fechaRegistro:date|None=Field(default=date.today())
    idComprador:int
    idVendedor:int
    costosEnvio:float
    subtotal:float
    estatus:str=Field(default="Captura")
    detalles:list[DetallePedido]

class Pago(BaseModel):
    fecha:date
    monto:float
    idTarjeta:int
    estatus:str

class PedidoPay(BaseModel):
    estatus:str
    pago:Pago