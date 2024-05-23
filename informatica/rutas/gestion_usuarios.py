from .rutas import informatica
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from autenticacion.modelos.modelos import rUsuario
from general.modelos.modelos import rPPUsuario, kPagina, kMenu, kSubMenu

from app import db

@informatica.route('/informatica/gestion-usuarios', methods=['POST', 'GET'])
def gestion_usuarios():
    return render_template('/modificar_usuario.html', title='Usuario',
                           current_user=current_user)



@informatica.route('/informatica/gestion-usuarios/crear-usuario', methods=['POST', 'GET'])
def crear_usuario():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        
        'idPersona' : 'idPersona',
        'Usuario' : 'Usuario',
        'Contrasena' : 'Contrasenia',
        'PrimerIngreso' : 'PrimerIngreso',
        'Activo' : 'Activo'
    }
    usuario_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    usuario_data["PrimerIngreso"] = 0
    usuario_data["Activo"] = 1
    nombre_usuario = usuario_data.get("Usuario", None)
    idPersona = usuario_data.get("idPersona", None)
    respuesta = {}
    if idPersona:    
        try:
            usuario_a_modificar = db.session.query(rUsuario).filter_by(Usuario = nombre_usuario).one()
            respuesta["existente"] = True
            respuesta["usuario"] = usuario_a_modificar.Usuario
            # for key, value in usuario_data.items():
            #     setattr(usuario_a_modificar, key, value)
            # respuesta["modificado"] = True
        except NoResultFound:
            usuario = rUsuario(**usuario_data)
            db.session.add(usuario)
            respuesta["creado"] = True
            respuesta["usuario"] = usuario_data["Usuario"]

        if respuesta.get('creado', False):
            dar_todos_los_permisos(nombre_usuario)

            # Realizar cambios en la base de datos
            db.session.commit()
    else:
        respuesta["noidPersona"] = True

    return jsonify(respuesta)

def dar_todos_los_permisos(Usuario):
    paginas = db.session.query(kPagina).all()

    # Eliminar permisos anteriores
    paginaUsuario = db.session.query(rPPUsuario).filter_by(Usuario = Usuario).delete()
    db.session.commit()
    
    pagina_data = {}
    pagina_data["Usuario"] = Usuario
    pagina_data["idPermiso"] = 1
    for pagina in paginas:
        pagina_data["idMenu"] = pagina.idMenu
        pagina_data["idSubMenu"] = pagina.idSubMenu
        pagina_data["idPagina"] = pagina.idPagina

        nueva_pagina = rPPUsuario(**pagina_data)
        db.session.add(nueva_pagina)
    print("permisos agregados")


@informatica.route('/informatica/gestion-usuarios/buscar-usuario', methods = ['POST', 'GET'])
def buscar_usuario():
     
    usuario_busq = request.form.get("BuscarUsuario")
    
    usuarios = db.session.query(rUsuario).filter(rUsuario.Usuario.contains(usuario_busq)).all()
    lista_usuarios = []
    for usuario in usuarios:
        if usuario is not None:
            usuario_dict = usuario.__dict__
            usuario_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_usuarios.append(usuario_dict)
    
    return jsonify(lista_usuarios)

@informatica.route('/informatica/gestion-usuarios/carga-arbol-paginas', methods=['POST', 'GET'])
def carga_arbol_paginas():
    paginas = db.session.query(kPagina).filter_by(Activo=1).all()

    lista_paginas = []
    for pagina in paginas:
        try:
            menu = db.session.query(kMenu).filter_by(idMenu = pagina.idMenu).one()
            submenu = db.session.query(kSubMenu).filter_by(idMenu = pagina.idMenu, idSubMenu = pagina.idSubMenu).one()
            pagina_data = {
                "Menu": menu.Menu,
                "SubMenu": submenu.SubMenu,
                "Pagina": pagina.Pagina,
                "URL": pagina.URL
            }
            lista_paginas.append(pagina_data)
        except NoResultFound:
            return jsonify({"error":True})
    print(lista_paginas)    
    return jsonify(lista_paginas)