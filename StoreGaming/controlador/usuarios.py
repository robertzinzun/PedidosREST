from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required,current_user,login_user,logout_user
import modelo


usuarios=Blueprint('usuarios',__name__)

@login_required
@usuarios.route('/usuarios')
def consultarUsuarios():
    if current_user.is_authenticated and current_user.is_admin():
        udao = modelo.Dao.UsuarioDAO()
        usuarios=udao.consultaGeneral(current_user.idUsuario)
        return render_template('usuarios/usuarios.html',usuarios=usuarios)
    else:
        abort(404)

@usuarios.route('/usuarios/nuevo')
def usuarioNuevo():
    if current_user.is_authenticated and not current_user.is_admin():
        return redirect(url_for("inicio"))
    else:
        msg=None
        return render_template('usuarios/registro.html',msg=msg)

@usuarios.route('/usuarios/registrar',methods=['post'])
def registrarUsuario():
    user= modelo.models.Usuario()
    user.nombreCompleto=request.form['nombre']
    user.email=request.form['email']
    user.password=request.form['password']
    user.direccion=request.form['direccion']
    user.telefono = request.form['telefono']
    if current_user.is_authenticated and current_user.is_admin():
        user.tipo=request.form['tipo']
    else:
        user.tipo='C'
    user.estatus='P'
    udao= modelo.Dao.UsuarioDAO()
    if( udao.existeCorreo(user.email)):
        msg={'estatus':'error','value':'El correo '+user.email+' ya esta en uso, intente con otro.'}
    else:
        if request.form['password']!=request.form['password2']:
            msg = {'estatus': 'error', 'value': 'Los password no coinciden.'}
        else:
            udao.registrar(user)
            msg = {'estatus': 'ok', 'value': 'Usuario agregado con exito, se ha enviado un correo a la direccion de correo proporcionada para confirmar la cuenta.'}
            mailer= modelo.Dao.MailSender()
            mailer.enviarEmail('Bienvenido a GamingStore','usuarios/confirmar',user)
    return render_template('usuarios/registro.html',msg=msg)

@usuarios.route('/login')
def login():
    msg=None
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    else:
        return render_template('login.html',msg=msg)

@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('usuarios.login'))

@usuarios.route('/usuarios/validar',methods=['POST'])
def validar():

    udao = modelo.Dao.UsuarioDAO()
    user=udao.validar(request.form['email'],request.form['password'])
    if user!=None:
        login_user(user)
        next = request.args.get('next')
        return redirect(next or url_for('inicio'))
    else:
        msg='Usuario invalido'
        return render_template('login.html',msg=msg)

@login_required
@usuarios.route('/usuarios/editarP')
def editarP():
    msg=None
    if current_user.is_authenticated:
        return render_template('usuarios/editarPerfil.html',msg=msg)
    else:
        return render_template('login.html', msg=msg)

@login_required
@usuarios.route('/usuarios/modificar',methods=['POST','GET'])
def modificar():
    msg=None
    if current_user.is_authenticated:
        user = modelo.models.Usuario()
        user.idUsuario=request.form['id']
        user.nombreCompleto = request.form['nombre']
        user.direccion = request.form['direccion']
        user.telefono = request.form['telefono']
        udao = modelo.Dao.UsuarioDAO()
        udao.modificar(user)
        msg = {'estatus': 'ok', 'value': 'Perfil modificado con exito.'}
        return render_template('usuarios/editarPerfil.html', msg=msg)
    else:
        abort(404)

@login_required
@usuarios.route('/usuarios/cambiarPassword')
def cambiarPassword():
    msg = None
    if current_user.is_authenticated:
        return render_template('usuarios/cambiarPassword.html', msg=msg)
    else:
        return render_template('login.html', msg=msg)

@login_required
@usuarios.route('/usuarios/guardarPassword',methods=['post','get'])
def guardarPassword():
    msg=None
    if current_user.is_authenticated:
        if current_user.validarPassword(request.form['password']) and request.form['passwordN']==request.form['passwordNC']:
            user=modelo.models.Usuario()
            user.idUsuario = request.form['id']
            user.password = request.form['passwordN']
            udao = modelo.Dao.UsuarioDAO()
            udao.modificar(user)
            msg={'estatus': 'ok', 'value': 'Password modificado con exito.'}
        else:
            msg = {'estatus': 'error', 'value': 'El valor de los password son incorrectos.'}
        return render_template('usuarios/cambiarPassword.html', msg=msg)
    else:
        return render_template('login.html', msg=msg)

@usuarios.route('/usuarios/confirmar/<int:id>')
def confirmar(id):
    msg=None
    user = modelo.models.Usuario()
    user.idUsuario = id
    user.estatus='A'
    udao = modelo.Dao.UsuarioDAO()
    udao.modificar(user)
    user=modelo.models.Usuario.query.get(id)
    return render_template('usuarios/confirmacion.html', user=user)

@usuarios.route('/usuarios/passwordOlvidado')
def passwordOlvidado():
    msg=None
    return render_template('usuarios/passwordOlvidado.html',msg=msg)

@usuarios.route('/usuarios/enviarpwd',methods=['post'])
def enviarpassword():
    email=request.form['email']
    udao = modelo.Dao.UsuarioDAO()
    if (udao.existeCorreo(email)):
        mailer = modelo.Dao.MailSender()
        user=udao.consultarPorEmail(email)
        mailer.enviarEmail('Envio de password', 'usuarios/envioPassword', user)
    return render_template('usuarios/respuestaPwd.html')

@usuarios.route('/usuarios/resetearpwd/<int:id>')
def resetear(id):
    msg=None
    return render_template('usuarios/reseteoPWD.html',id=id,msg=msg)

@usuarios.route('/usuarios/actualizarPwd',methods=['POST'])
def actualizarPwd():
    msg=None
    if request.form['passwordN'] == request.form['passwordNC']:
        user = modelo.models.Usuario()
        user.idUsuario = request.form['id']
        user.password = request.form['passwordN']
        udao = modelo.Dao.UsuarioDAO()
        udao.modificar(user)
        msg = {'estatus': 'ok', 'value': 'Password reseteado con exito, ahora puedes iniciar sesion.'}
    else:
        msg = {'estatus': 'error', 'value': 'El valor de los password son incorrectos.'}
    return render_template('usuarios/reseteoPwd.html', msg=msg)

@usuarios.route('/usuarios/eliminar/<int:id>')
def eliminarUsuario(id):
    udao = modelo.Dao.UsuarioDAO()
    udao.eliminar(id)
    return redirect(url_for('usuarios.consultarUsuarios'))

@login_required
@usuarios.route('/usuarios/editar/<int:id>')
def editarUsuario(id):
    msg=None
    if current_user.is_authenticated and current_user.is_admin():
        udao = modelo.Dao.UsuarioDAO()
        usuario=udao.consultaIndividual(id)
        return render_template('usuarios/usuario.html',usuario=usuario,msg=msg)
    else:
        abort(404)

@login_required
@usuarios.route('/usuarios/guardar',methods=['POST'])
def guardarUsuario():
    msg = None
    if current_user.is_authenticated and current_user.is_admin():
        user = modelo.models.Usuario()
        user.idUsuario = request.form['id']
        user.nombreCompleto = request.form['nombre']
        user.direccion = request.form['direccion']
        user.telefono = request.form['telefono']
        user.tipo=request.form['tipo']
        user.estatus=request.values.get("estatus","B")
        if(request.form['password']):
            print(request.form['password'])
            user.password=request.form['password']
        udao = modelo.Dao.UsuarioDAO()
        udao.modificar(user)
        return redirect(url_for('usuarios.consultarUsuarios'))
    else:
        abort(404)




