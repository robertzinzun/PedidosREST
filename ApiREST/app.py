from flask import Flask,request,jsonify,render_template,redirect,url_for
from flask_bootstrap import Bootstrap
import json
from model import Opcion,Usuario
import requests
from flask_login import login_user,login_required,LoginManager,logout_user
app=Flask(__name__)
Bootstrap(app)
app.secret_key='clave'
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(id):
    u=Usuario()
    return u
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login',methods=['post'])
def iniciarSesion():
    u=Usuario()
    u.id=1
    u.nombre=request.form['email']
    login_user(u)
    return render_template('principal.html')

@app.route('/nuevoUsuario')
def nuevoUsuario():
    return render_template('registroUsuarios.html')

@app.route('/cerrarSesion')
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))

@app.route('/opciones',methods=['GET'])
def consulta():
    o=Opcion()
    respuesta=o.consultaGeneral()
    return render_template('consultaOpciones.html',resp=respuesta)

@app.route('/opciones/<int:id>',methods=['GET'])
def consulta_opcion(id):
    opciones={"id":id,"nombre":"Tesis","descripcion":"Informe de Tesis"}
    return json.dumps(opciones)

@app.route('/opciones',methods=['POST'])
def agregarOpcion():
    opcion=request.get_json()
    print(opcion['nombre'])
    return opcion

@app.route('/opciones',methods=['PUT'])
def editarOpcion():
    opcion=request.get_json()
    print(opcion['nombre'])
    return opcion

@app.route('/opciones/<int:id>',methods=['DELETE'])
def eliminarOpcion(id):
    return ('Eliminando la opcion')

@app.route('/solicitudes',methods=['get'])
def consultarSolicitudes():
    url='http://172.16.1.135:8000/solicitudes/1'
    resp=requests.get(url)
    return render_template('solicitud.html',resp=resp.json())

if __name__=='__main__':
    app.run(debug=True)