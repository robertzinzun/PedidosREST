from pydantic import BaseModel,Field
from datetime import datetime

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
    detalles:list[DetallePedido]

class Pago(BaseModel):
    fecha:datetime=Field(default=datetime.now())
    monto:float=Field(ge=0)
    idTarjeta:int
    estatus:str=Field(default='Aprobado')

class PedidoPay(BaseModel):
    estatus:str=Field(default='Pagado')
    pago:Pago