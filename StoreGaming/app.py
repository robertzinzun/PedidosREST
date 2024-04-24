from flask import Flask, render_template,request,url_for,redirect,abort,session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from flask_mail import Mail
from datetime import timedelta

import config
import controlador.categorias
import controlador.productos
import controlador.usuarios

import modelo.Dao
import modelo.models

app=Flask(__name__)
app.config.from_object(config)
db=SQLAlchemy(app)
Bootstrap(app)
mail=Mail(app)

login_manager=LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view="login"
login_manager.refresh_view="login"
login_manager.needs_refresh_message=("Tu sesión ha expirado, por favor inicia nuevamente tu sesión")
login_manager.needs_refresh_message_category="info"


app.register_blueprint(controlador.categorias.categorias)
app.register_blueprint(controlador.productos.productos)
app.register_blueprint(controlador.usuarios.usuarios)

@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@login_manager.user_loader
def load_user(user_id):
    udao=modelo.Dao.UsuarioDAO()
    return udao.consultaIndividual(int(user_id))

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',error="Error interno en la aplicación"), 500
@app.route('/hola')
def hola():
    return "Hola mundo"
if __name__=="__main__":
    app.run(host='0.0.0.0')
