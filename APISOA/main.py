from flask import Flask
from model.DAO import Categoria,Producto,db,Pedido

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userShopiteszSOA:Shopitesz.123@localhost/shopiteszSOA'
@app.route('/')
def inicio():
    return {"estatus":"OK","mensaje":"Hola mundo"}
# Press the green button in the gutter to run the script.
@app.route('/categorias',methods=['get'])
def consultarCategorias():
    cat=Categoria()
    return cat.consultar()

@app.route('/productos',methods=['get'])
def consultarProductos():
    prod=Producto()
    prod.view()
    return prod.consultar()
@app.route('/pedidos/<int:idPedido>',methods=['Get'])
def consultarPedido(idPedido):
    pedido=Pedido()
    return pedido.consultaIndividual(idPedido)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
