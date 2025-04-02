from pymongo import MongoClient
MONGO_URI='mongodb://localhost:27017'
DATABASE='ShopiteszREST'
class Conexion:
    def __init__(self):
        self.client=MongoClient(MONGO_URI)
        self.db=self.client[DATABASE]
    def cerrar(self):
        self.client.close()
    def getDB(self):
        return self.db