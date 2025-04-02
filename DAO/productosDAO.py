from DAO.database import Conexion
from models import ProductosSalida
class ProductoDAO:
    def consultaGeneral(self):
        cn=Conexion()
        result=cn.getDB().productos.find({})
        print(result)
        lista=list(result)
        salida=ProductosSalida(productos=lista)
        cn.cerrar()
        return salida