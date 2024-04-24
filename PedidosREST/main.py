# This is a sample Python script.
from fastapi import FastAPI
import uvicorn
from models import PedidoInsert,PedidoPay
from dao import Conexion
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
app=FastAPI()
#Evento que indica el momento en que se crea una una conexion con la BD
@app.on_event('startup')
def startup():
    app.cn=Conexion()
    print('Conectando con la BD')

@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
    print('Cerrando la conexion')
@app.get('/categorias')
def consultaGeneralCategorias():
    return app.cn.consultaCategorias()
@app.get('/')
def inicio():
    return {"mensaje":"Bienvenido a PedidosREST"}

@app.post('/pedidos')
def agregarPedido(pedido:PedidoInsert):
    #return {"mensaje":"Agregando un pedido"}
    salida=app.cn.agregarPedido(pedido)
    return salida
@app.put('/pedidos/{idPedido}/pagar')
def pagarPedido(idPedido:str,pedidoPay:PedidoPay):
    #return {"mensaje":f"Pagando el pedido con id:{idPedido}"}
    salida=app.cn.pagarPedido(idPedido,pedidoPay)
    return salida

@app.delete('/pedidos/{idPedido}/cancelar')
def candelarPedido(idPedido:str):
    return {"mensaje":f"Cancelando el pedido con id:{idPedido}"}

@app.get('/pedidos')
def consultaGeneralPedidos():
    lista=[{"idPedido":"1","total":100},{"idPedido":"2","total":150},
           {"idPedido":"3","total":200}]
    return lista


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",port=8000,reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
