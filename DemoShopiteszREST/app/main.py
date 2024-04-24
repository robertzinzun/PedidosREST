# This is a sample Python script.
from fastapi import FastAPI,status,HTTPException,Depends
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import uvicorn
from datetime import datetime
from pydantic import BaseModel, Field
from dao.conexion import Conexion
from typing import List,Annotated,Any
from app.models.schemas import Categoria,Usuario,PedidoInsert


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
app=FastAPI()
security=HTTPBasic()
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.on_event("startup")
def startup():
    print('Conectando con la BD')
    app.cn=Conexion()
@app.on_event('shutdown')
def shutdown():
    print('Cerrando conexion')
    if app.cn!=None:
        app.cn.cerrar()
@app.get('/')
async def  inicio():
    return {"estatus":"OK","mensaje":"Bienvenido a ShopiteszREST"}
@app.get('/pedidos/{idPedido}')
async def consultarPedido(idPedido:int):
    return {"idPedido":idPedido,"mensaje":"consultando el pedido "+str(idPedido)}

@app.post("/items/{item_id}")
async def create_item(item: Item,item_id:int):
    print(item_id)
    return item

@app.post(path='/pedidos',summary="Agregar Pedido")
def agregarPedido(pedido:PedidoInsert):
    return pedido

def get_user(credenciales:HTTPBasicCredentials=Depends(security))->Usuario:
    res=app.cn.validarUsuario(credenciales.username,credenciales.password)
    if res:
        return Usuario(**res)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Usuario no autorizado')

@app.get('/categorias',response_model=List[Categoria],status_code=status.HTTP_200_OK)
def consultarCategorias():
    # print(current_user.tipo)
    # if current_user is None:
    #     raise(HTTPException(status.HTTP_401_UNAUTHORIZED,detail='No autorizado'))
    return app.cn.consultarCategorias()
@app.post('/categorias',description="Agregar una Categoria")
def agregarCategoria(cat:Categoria)->Categoria:
    print(cat)

    raise HTTPException(status.HTTP_404_NOT_FOUND,detail={"mensaje":"No encontrado"})
    return cn.agregarCategoria(cat)


@app.get('/login',response_model=Usuario)
def validarUsuario(current_user:Usuario=Depends(get_user))->Any:
    return current_user


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
