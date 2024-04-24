from flask import Blueprint,render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
import modelo

categorias = Blueprint('categorias',__name__)

@categorias.route('/categorias')
def consultarCategorias():
    cdao = modelo.Dao.CategoriaDAO()
    categorias = cdao.consultaGeneral()
    return render_template('categorias/categorias.html', categorias=categorias)
@categorias.route('/categorias/<int:id>')
@login_required
def consultarCategoria(id=0):
    cdao = modelo.Dao.CategoriaDAO()
    categoria=cdao.consultaIndividual(id)
    return render_template('categorias/categoria.html',categoria=categoria)
@categorias.route('/categorias/nueva')
@login_required
def nuevaCategoria():
    if current_user.is_admin():
        return render_template('categorias/categoriaNueva.html')
    else:
        abort(404)
@categorias.route('/categorias/insertar',methods=['post'])
def insertarCategoria():
    cat=modelo.models.Categoria()
    cat.nombre=request.form['nombre']
    cdao = modelo.Dao.CategoriaDAO()
    cdao.insertar(cat)
    return redirect(url_for('categorias.consultarCategorias'))
@categorias.route('/categorias/modificar',methods=['post'])
def modificarCategoria():
    cat = modelo.models.Categoria()
    cat.idCategoria=request.form['id']
    cat.nombre=request.form['nombre']
    cdao = modelo.Dao.CategoriaDAO()
    cdao.modificar(cat)
    return redirect(url_for('categorias.consultarCategorias'))
@categorias.route('/categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id=0):
    cdao = modelo.Dao.CategoriaDAO()
    cdao.eliminar(id)
    return redirect(url_for('categorias.consultarCategorias'))
@categorias.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404