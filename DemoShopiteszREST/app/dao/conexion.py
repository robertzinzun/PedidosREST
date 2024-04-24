from pymongo import MongoClient
from app.models.schemas import CategoriasCol,Categoria,Usuario

bd=None
class Conexion():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.ShopiteszREST
    def consultarCategorias(self):
        categorias=list(self.bd.categorias.find())
        return categorias
    def agregarCategoria(self,categoria:Categoria):
        self.bd.categorias.insert_one(categoria.dict())
        return categoria
    def validarUsuario(self,email,password):
        res=self.bd.usuarios.find_one({"email":email,"password":password})
        return res
    def cerrar(self):
        self.cliente.close()


