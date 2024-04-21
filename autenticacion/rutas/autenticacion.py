from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app import db
from autenticacion.modelos.modelos import User, rUsuario, rPPUsuario, kMenu, kSubMenu, kPagina
# from app import app_instance
from sqlalchemy.orm.exc import NoResultFound
from general.herramientas.funciones import permisos_de_consulta
from app import app

autenticacion = Blueprint('autenticacion', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/scripts')


@autenticacion.route('/')
def inicio_sesion():
    if current_user.is_authenticated:
        return redirect(url_for('principal.SIA'))
    return render_template('/inicio_sesion.html', tittle = 'Sistema Integral Administrativo',
                           current_user = None)

@autenticacion.route('/autenticacion/iniciar-sesion', methods = ['POST'])
def login():
    usuario = request.form['Usuario']
    contrasena = request.form['Contrasena']
    user_db = db.session.query(rUsuario).filter_by(Usuario=usuario).first()
    if user_db and user_db.Contrasenia == contrasena:
        user = User(user_db)
        if user_db.Activo == 1:
            # Establece el valor de 'hora_inicio' en la sesión cuando el usuario inicia sesión
            session['hora_inicio'] = datetime.now(timezone.utc).isoformat()
            session['tiempo_sesion'] = app.config["PERMANENT_SESSION_LIFETIME"].total_seconds()
            login_user(user)

            idPaginasUsuario = db.session.query(rPPUsuario).filter(rPPUsuario.idUsuario==user_db.idUsuario).all()
            print(len(idPaginasUsuario))
            print((idPaginasUsuario))
            paginas_usuario = []
            pagina={}
            # CREAR MENU
            for PaginaUsuario in idPaginasUsuario:
                try:
                    menu = db.session.query(kMenu).filter_by(idMenu=PaginaUsuario.idMenu).one() #
                    submenu = db.session.query(kSubMenu).filter_by(idMenu=PaginaUsuario.idMenu, idSubMenu=PaginaUsuario.idSubMenu).one() #
                    pag = db.session.query(kPagina).filter_by(idMenu=PaginaUsuario.idMenu, idSubMenu=PaginaUsuario.idSubMenu, idPagina = PaginaUsuario.idPagina).one() #

                    pagina={}
                    pagina["Menu"] = menu.Menu
                    pagina["SubMenu"] = submenu.SubMenu
                    pagina["Pagina"] = pag.Pagina
                    pagina["URL"] = pag.URL
                    pagina["Activo"] = pag.Activo
                    # pagina["Menu"] = PaginaUsuario.Pagina.SubMenu.Menu.Menu
                    # pagina["SubMenu"] = PaginaUsuario.Pagina.SubMenu.SubMenu
                    # pagina["Pagina"] = PaginaUsuario.Pagina.Pagina
                    # pagina["URL"] = PaginaUsuario.Pagina.URL
                    # pagina["Activo"] = PaginaUsuario.Pagina.Activo
                    pagina["idPermiso"] = 1

                    print(PaginaUsuario.Pagina.SubMenu.idSubMenu)

                    paginas_usuario.append(pagina)
                except NoResultFound:
                    pass
                
            session['paginas_usuario'] = paginas_usuario
            
            if user_db.PrimerIngreso == 0:
                return jsonify({"logged": True, "PrimeraVez": True})
            return jsonify({"logged": True})
        
        return jsonify({"logged": "Inactivo"})
    else:
        if user_db:
            return jsonify({"logged": "ContrasenaIncorrecta"})
        else:
            return jsonify({"logged": "UsuarioIncorrecto"})



# Agregar usuarios (falta plantilla)      
# @autenticacion.route('/sign', methods = ['POST'])
# def sign_in():
#     usuario = request.form['Usuario']
#     contrasena = request.form['Contrasena']

#     user = User()
#     user.Usuario = usuario
#     user.Contrasenia = contrasena
    
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"logged": True})

@autenticacion.route('/autenticacion/cerrar-sesion')
def logout():
    if current_user:
        logout_user()
    return redirect(url_for('autenticacion.inicio_sesion'))

@autenticacion.route('/autenticacion/actualiza-sesion', methods=['POST'])
def actualiza_sesion():
    session['hora_inicio'] = datetime.now(timezone.utc).isoformat()
    return jsonify({"actualizado": True, 'nueva_hora_inicio': session['hora_inicio']})


@autenticacion.route('/autenticacion/cambia-contrasena', methods=['POST', 'GET'])
@permisos_de_consulta
def cambia_contrasena():
    return render_template('/cambia_contrasena.html', title='Cambia contraseña',
                           current_user=current_user)

@autenticacion.route('/autenticacion/cambiar-contrasena', methods=['POST', 'GET'])
@permisos_de_consulta
def cambiar_contrasena():
    respuesta = {}
    ContrasenaActual = request.form['ContrasenaActual']
    NuevaContrasena = request.form['NuevaContrasena']
    NuevaContrasena2 = request.form['NuevaContrasena2']

    usuario_actual = db.session.query(rUsuario).filter_by(idPersona=current_user.idPersona).first()

    if (ContrasenaActual == usuario_actual.Contrasenia):
        respuesta["ContrasenaActual"] = True

        if (NuevaContrasena == NuevaContrasena2):
            respuesta["NuevasContrasenasCoinciden"] = True
            
            usuario_actual.Contrasenia = NuevaContrasena

            usuario_actual.PrimerIngreso = 1# datetime.now().date()
            db.session.commit()
            respuesta["CambioContrasena"] = True

    return jsonify(respuesta)


@autenticacion.route('/permisos-usuario', methods=['POST', 'GET'])
def permisos_usuario():
    return render_template('/permisos_usuario.html', title='Usuario',
                           current_user=current_user)