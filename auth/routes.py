from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app import db
from auth.models import User, Tusuario
# from app import app_instance
from sqlalchemy.orm.exc import NoResultFound
from general.utils.funciones import permisos_de_consulta
from app import app

auth = Blueprint('auth', __name__, template_folder = 'templates', static_folder='static', static_url_path='/scripts')


@auth.route('/')
def index():
    return render_template('/index.html', tittle = 'Sistema Integral Administrativo')

@auth.route('/login', methods = ['POST'])
def login():
    usuario = request.form['Usuario']
    contrasena = request.form['Contrasena']
    user_db = db.session.query(Tusuario).filter_by(usuario=usuario).first()
    if user_db and user_db.contrasena == contrasena:
        user = User(user_db)
        if user_db.estatus == 1:
            # Establece el valor de 'hora_inicio' en la sesión cuando el usuario inicia sesión
            session['hora_inicio'] = datetime.now(timezone.utc).isoformat()
            session['tiempo_sesion'] = app.config["PERMANENT_SESSION_LIFETIME"].total_seconds()
            login_user(user)
            return jsonify({"logged": True})
        
        return jsonify({"logged": "Inactivo"})
    else:
        if user_db:
            return jsonify({"logged": "ContrasenaIncorrecta"})
        else:
            return jsonify({"logged": "UsuarioIncorrecto"})

# Agregar usuarios (falta plantilla)      
# @auth.route('/sign', methods = ['POST'])
# def sign_in():
#     usuario = request.form['Usuario']
#     contrasena = request.form['Contrasena']

#     user = User()
#     user.usuario = usuario
#     user.contrasena = contrasena
#     user.idRol = 1
    
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"logged": True})

@auth.route('/logout')
@login_required
def logout():
    session["idPersona"] = None
    logout_user()
    return redirect(url_for('auth.index'))

@auth.route('/actualiza_sesion', methods=['POST'])
def actualiza_sesion():
    session['hora_inicio'] = datetime.now(timezone.utc).isoformat()
    return jsonify({"actualizado": True, 'nueva_hora_inicio': session['hora_inicio']})


@auth.route('/cambia_contrasena', methods=['POST', 'GET'])
@permisos_de_consulta
def cambia_contrasena():
    print(current_user.idPersona)
    return render_template('/cambiaContrasena.html', title='Cambia contraseña',
                           current_user=current_user)

@auth.route('/cambiar_contrasena', methods=['POST', 'GET'])
@permisos_de_consulta
def cambiar_contrasena():
    respuesta = {}
    ContrasenaActual = request.form['ContrasenaActual']
    NuevaContrasena = request.form['NuevaContrasena']
    NuevaContrasena2 = request.form['NuevaContrasena2']

    usuario_actual = db.session.query(Tusuario).filter_by(idPersona=current_user.idPersona).first()

    if (ContrasenaActual == usuario_actual.contrasena):
        respuesta["ContrasenaActual"] = True

        if (NuevaContrasena == NuevaContrasena2):
            respuesta["NuevasContrasenasCoinciden"] = True
            
            usuario_actual.ultimacontrasena = ContrasenaActual
            usuario_actual.contrasena = NuevaContrasena
            db.session.commit()
            respuesta["CambioContrasena"] = True



    return jsonify(respuesta)
