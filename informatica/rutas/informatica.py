from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from autenticacion.modelos.modelos import rUsuario
from general.modelos.modelos import rPPUsuario, kPagina

from app import db

informatica = Blueprint('informatica', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/informatica/estatico')

@informatica.route('/informatica/gestion-usuarios', methods=['POST', 'GET'])
def gestion_usuarios():
    return render_template('/modificar_usuario.html', title='Usuario',
                           current_user=current_user)



@informatica.route('/informatica/crear-usuario', methods=['POST', 'GET'])
def crear_usuario():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        
        'idPersona' : 'idPersona',
        'idUsuario' : 'idUsuario',
        'Usuario' : 'Usuario',
        'Contrasena' : 'Contrasenia',
        'PrimerIngreso' : 'PrimerIngreso',
        'Activo' : 'Activo'
    }
    usuario_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    usuario_data["idPersona"] = 0
    usuario_data["PrimerIngreso"] = 1
    usuario_data["Activo"] = 1
    idUsuario = usuario_data.get("idUsuario", None)
    
    respuesta = {}
    try:
        usuario_a_modificar = db.session.query(rUsuario).filter_by(idUsuario = idUsuario).one()
        for key, value in usuario_data.items():
            setattr(usuario_a_modificar, key, value)
        respuesta["modificado"] = True
    except NoResultFound:
        
        ultimo_idUsuario = db.session.query(func.max(rUsuario.idUsuario)).scalar()
        if ultimo_idUsuario:
            idUsuario = ultimo_idUsuario + 1
        else:
            idUsuario = 1
        usuario_data["idUsuario"] = idUsuario

        usuario = rUsuario(**usuario_data)
        db.session.add(usuario)
        respuesta["creado"] = True

    # Realizar cambios en la base de datos
    db.session.commit()

    dar_todos_los_permisos(idUsuario)

    return jsonify(respuesta)

def dar_todos_los_permisos(idUsuario):
    paginas = db.session.query(kPagina).all()

    pagina_data = {}
    pagina_data["idUsuario"] = idUsuario
    pagina_data["idPermiso"] = 1
    for pagina in paginas:
        pagina_data["idMenu"] = pagina.idMenu
        pagina_data["idSubMenu"] = pagina.idSubMenu
        pagina_data["idPagina"] = pagina.idPagina

        nueva_pagina = rPPUsuario(**pagina_data)
        db.session.add(nueva_pagina)
    db.session.commit()
    print("permisos agregados")
