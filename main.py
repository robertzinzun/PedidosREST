# This is a sample Python script.
from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn
from models import PedidoInsert,PedidoPay,PedidoCancelado,PedidosConsulta,PedidoConsulta,Respuesta,UsuarioSalida
from dao import Conexion
from fastapi.responses import JSONResponse,Response,Any
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
app=FastAPI()
security=HTTPBasic()
#Evento que indica el momento en que se crea una una conexion con la BD
@app.on_event('startup')
def startup():
    app.cn=Conexion()
    print('Conectando con la BD')

@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
    print('Cerrando la conexion')
@app.get('/categorias',summary="Consulta de Categorias",description="Categorias",tags=["Categorias"])
def consultaGeneralCategorias():
    return app.cn.consultaCategorias()
@app.get('/')
def inicio():
    return {"mensaje":"Bienvenido a PedidosREST"}

def autenticar(credenciales:HTTPBasicCredentials=Depends(security))->UsuarioSalida:
    try:
        salida=app.cn.autenticar(credenciales.username,credenciales.password)
        return UsuarioSalida(**salida)
    except:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail={"mensaje":"Usuario no autorizado"})

@app.get('/usuarios/autenticar',response_model=UsuarioSalida,tags=["Usuario"])
def login(usuario:UsuarioSalida=Depends(autenticar))->Any:
    return usuario



@app.post('/pedidos',response_model=Respuesta,summary="Registro de un pedido",tags=["Pedidos"])
def agregarPedido(pedido:PedidoInsert)->Any:
    #return {"mensaje":"Agregando un pedido"}
    salida=app.cn.agregarPedido(pedido)
    return Respuesta(**salida)

@app.put('/pedidos/{idPedido}/pagar',summary="Pago de un pedido",response_model=Respuesta,tags=["Pedidos"])
def pagarPedido(idPedido:str,pedidoPay:PedidoPay)->Any:
    #return {"mensaje":f"Pagando el pedido con id:{idPedido}"}
    salida=app.cn.pagarPedido(idPedido,pedidoPay)
    return Respuesta(**salida)

@app.delete('/pedidos/{idPedido}/cancelar',summary='Cancelación de un pedido',response_model=Respuesta,tags=["Pedidos"])
def cancelarPedido(idPedido:str,pedido:PedidoCancelado,
                   usuario:UsuarioSalida=Depends(autenticar))->Any:
    #return {"mensaje":f"Cancelando el pedido con id:{idPedido}"}
    if usuario.estatus=='OK' and usuario.usuario.tipo=='Comprador':
        salida=app.cn.cancelarPedido(idPedido,pedido,usuario.usuario.idUsuario)
        return Respuesta(**salida)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail={"mensaje":"Usuario no autorizado"})

@app.get('/pedidos',response_model=PedidosConsulta,summary=" Consulta general de pedidos",tags=["Pedidos"])
def consultaGeneralPedidos(usuario:UsuarioSalida=Depends(autenticar))->Any:
    print(usuario)
    if usuario.estatus=="OK" and (usuario.usuario.tipo=='Administrador' or
                                  usuario.usuario.tipo=="Comprador" or
                                  usuario.usuario.tipo=="Vendedor"):
        salida=app.cn.consultaGeneralPedidos()
        return PedidosConsulta(**salida)
    else:
       return usuario

@app.get('/pedidos/{idPedido}',response_model=PedidoConsulta,summary="Consulta de un pedido",tags=["Pedidos"])
def consultarPedido(idPedido:str)->Any:
    salida=app.cn.consultarPedido(idPedido)
    return PedidoConsulta(**salida)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",port=8000,reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
