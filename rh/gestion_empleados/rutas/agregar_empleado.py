from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
import os

from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
#from catalogos.modelos.modelos import *
from app import db
from general.herramientas.funciones import *

@gestion_empleados.route('/rh/gestion-empleados/busqueda-empleado', methods = ['POST', 'GET'])
def busqueda_empleado():
    session["idPersona"] = None
    return render_template('/buscarempleado.html', title='Búsqueda de empleado',
                           current_user=current_user)

@gestion_empleados.route('/rh/gestion-empleados/agregar-empleado', methods = ['POST', 'GET'])
@gestion_empleados.route('/rh/gestion-empleados/modificar-empleado', methods = ['POST', 'GET'])
def modificar_empleado():
    if request.path == '/rh/gestion-empleados/modificar-empleado':
            idSelec = session.get("idPersona",None)
            if idSelec is None:
                return redirect('/rh/gestion-empleados/agregar-empleado')
            titulo = "Modifica empleado"
    else:
            #if current_user.idRol == 2 :
            #    return redirect('/rh/gestion-empleados/busqueda-empleado')
            idSelec = None
            session["idPersona"] = None
            titulo = "Agrega empleado"
    empleado  = db.session.query(tPersona).filter_by(idPersona = idSelec).first()

    # Catalogos para el empleado
    TipoPersona_datos = db.session.query(kTipoPersona).filter_by(Activo = 1).order_by(kTipoPersona.idTipoPersona).all()
    EstCiv_datos = db.session.query(kEstadoCivil).filter_by(Activo = 1).order_by(kEstadoCivil.idEstadoCivil).all()
    Nacionalidad_datos = db.session.query(kNacionalidad).filter_by(Activo = 1).order_by(kNacionalidad.idNacionalidad).all()
    TipoEmpleado_datos = db.session.query(kTipoEmpleado).filter_by(Activo = 1).order_by(kTipoEmpleado.idTipoEmpleado).all()
    CentroCostos_datos = db.session.query(kCentroCostos).order_by(kCentroCostos.idCentroCosto).all()
    Quincena_datos = db.session.query(kQuincena).order_by(kQuincena.idQuincena).all()
    Escolaridad_datos = db.session.query(kEscolaridad).filter_by(Activo = 1).order_by(kEscolaridad.idEscolaridad).all()

    # Catalogos para el domicilio
    Entidad_datos = db.session.query(kEntidad).filter_by(Activo = 1).order_by(kEntidad.idEntidad).all()
    TipoAsentamiento_datos = db.session.query(kTipoAsentamiento).filter_by(Activo = 1).order_by(kTipoAsentamiento.idTipoAsentamiento).all()
    Vialidad_datos = db.session.query(kVialidad).filter_by(Activo = 1).order_by(kVialidad.idVialidad).all()

    return render_template('/datos_bancarios.html', title = titulo,
                           current_user = current_user,
                           TipoPersona = TipoPersona_datos,
                           EstCiv = EstCiv_datos,
                           Nacionalidad = Nacionalidad_datos,
                           TipoEmpleado = TipoEmpleado_datos,
                           CentroCostos = CentroCostos_datos,
                           Quincena = Quincena_datos,
                           Escolaridad = Escolaridad_datos,
                           Entidad = Entidad_datos,
                           TipoAsentamiento = TipoAsentamiento_datos,
                           Vialidad = Vialidad_datos,
                           empleado = empleado)

@gestion_empleados.route('/rh/gestion-empleados/guarda-empleado', methods = ['POST'])
def guardar_empleado():
    mapeo_nombres_persona = { #NombreEnFormulario : nombreEnBase
        'CURP': 'CURP',
        'Nombre': 'Nombre',
        'Paterno': 'ApPaterno',
        'Materno': 'ApMaterno',
        'Sexo': 'Sexo',
        'FechaNacimiento_format': 'FechaNacimiento',
        'RFC': 'RFC',
        'idEstadoCivil': 'idEstadoCivil',
        'idNacionalidad': 'idNacionalidad',
        'CalidadMigratoria': 'CalidadMigratoria',
        'TelCasa': 'TelCasa',
        'TelCelular': 'TelCelular',
        'idTipoPersona': 'idTipoPersona',
        #'CorreoPersonal': 'CorreoPersonal',
        #'CorreoInstitucional': 'CorreoInstitucional',
        #'idTipoEmpleo': 'idTipoEmpleo',
        #'idTipoAlta': 'idTipoAlta',
        #'idGrupo': 'idGrupo',
        #'idPuesto': 'idPuesto',
        #'idPuestoJefe': 'idPuestoJefe',
        #'idCentroCosto': 'idCentroCosto',
        #'HoraEntrada': 'HoraEntrada',
        #'HoraSalida': 'HoraSalida',
        #'FecIngresoGob_format': 'FecIngresoGob',
        #'FecIngreso_format': 'FecIngreso',
        #'MesesServicio': 'MesesServicio',
        #'idEscolaridad': 'idEscolaridad',
        #'idNivelEscolaridad': 'idNivelEscolaridad',
        #'idInstitucionEscolar': 'idInstitucionEscolar',
        #'idFormacionEducativa': 'idFormacionEducativa',
        #'Especialidad': 'Especialidad',
        #'NumQuincena': 'NumQuincena',
        #'Clabe': 'Clabe',
        #'Banco': 'Banco',
        #'idEstatus': 'Activo',
    }

    mapeo_nombres_empleado = {
        'idTipoEmpleo': 'idTipoEmpleado',
    }

    mapeo_nombres_empleado_puesto = {
        'idPlazaHom' : 'idPuesto'
    }

    persona_data = {mapeo_nombres_persona[key]: request.form.get(key) for key in mapeo_nombres_persona.keys()}
    empleado_data = {mapeo_nombres_empleado[key]: request.form.get(key) for key in mapeo_nombres_empleado.keys()}
    empleado_puesto_data = {mapeo_nombres_empleado_puesto[key]: request.form.get(key) for key in mapeo_nombres_empleado_puesto.keys()}

    print(persona_data)
    print(empleado_data)
    print(empleado_puesto_data)

    idPersona = session.get("idPersona", None)
    nueva_persona = None
    nuevo_empleado = None
    nuevo_empleado_puesto = None
    correo_enviado = False
    respuesta = {}


    try:
        empleado_existente = db.session.query(tPersona).filter_by(idPersona=idPersona).one()
        existe = 1
        # Si llegamos aquí, significa que ya existe un empleado
        # Envía correo correspondiente
        # if not(empleado_existente.Activo == int(empleado_data["Activo"])):
        #     if(int(empleado_data["Activo"]) == 1):
        #         envia_correo("informatica","Reactivar",empleado_existente)
        #         crea_solicitud("Reactivar",empleado_existente)
        #         correo_enviado = True
        #     if(int(empleado_data["Activo"]) == 0):
        #         envia_correo("informatica","Baja",empleado_existente)
        #         crea_solicitud("Baja",empleado_existente)
        #         correo_enviado = True

        # Actualizar los atributos de 'empleado_existente' con los valores de 'empleado_data'
        for attr, value in persona_data.items():
            if not attr.startswith('_') and hasattr(empleado_existente, attr):
                setattr(empleado_existente, attr, value)

    except NoResultFound:
        # Obtener el último valor de idPersona de la tabla de empleados y sumarle 1
        ultimo_id = db.session.query(func.max(tPersona.idPersona)).scalar()
        existe = 0
        if ultimo_id is None:
            nuevo_id_persona = 1
        else:
            nuevo_id_persona = ultimo_id + 1
            
        ultimo_Numero_Empleado = db.session.query(func.max(rEmpleado.NumeroEmpleado)).scalar()
        if ultimo_Numero_Empleado is None:
            nuevo_Numero_Empleado = 1
        else:
            nuevo_Numero_Empleado = ultimo_Numero_Empleado + 1

        # Asignar el nuevo valor de idPersona y NumeroEmpleado
        persona_data['idPersona'] = nuevo_id_persona
        empleado_data['idPersona'] = nuevo_id_persona
        empleado_data['NumeroEmpleado'] = nuevo_Numero_Empleado
        empleado_puesto_data['idPersona'] = nuevo_id_persona

        empleado_data['Activo'] = 1

        nueva_persona = tPersona(**persona_data)
        db.session.add(nueva_persona)
        print(nueva_persona)
        nuevo_empleado = rEmpleado(**empleado_data)
        db.session.add(nuevo_empleado)
        print(nuevo_empleado)
        nuevo_empleado_puesto = rEmpleadoPuesto(**empleado_puesto_data)
        db.session.add(nuevo_empleado_puesto)
        print(nuevo_empleado_puesto)
        respuesta["guardado"] = True

    # Realizar cambios en la base de datos
    db.session.commit()

    return jsonify(respuesta)

@gestion_empleados.route('/rh/gestion-empleados/buscar-empleado', methods = ['POST', 'GET'])
def buscar_empleado():
     
    parametro = request.form.get("WParametro")
    esModal = request.form.get("esModal")

    filtro_comun = or_(
        tPersona.CURP.contains(parametro),
        tPersona.Nombre.contains(parametro),
        tPersona.ApPaterno.contains(parametro),
        tPersona.ApMaterno.contains(parametro),
        #rEmpleado.NumeroEmpleado.contains(parametro)
    )

    #if esModal:
        #filtro_comun = and_(filtro_comun, tPersona.Empleado.Activo == 1)

    empleados = db.session.query(tPersona).filter(filtro_comun).all()
    lista_empleados = []
    for empleado in empleados:
        if empleado is not None:
            NumeroEmpleado = empleado.Empleado.NumeroEmpleado
            empleado_dict = empleado.__dict__
            empleado_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            empleado_dict["NumeroEmpleado"] = NumeroEmpleado
            empleado_dict.pop("Empleado")
            lista_empleados.append(empleado_dict)
    return jsonify(lista_empleados)


@gestion_empleados.route('/rh/gestion-empleados/buscar-curp', methods = ['POST'])
def buscar_curp():
    curp = request.form.get("CURP")
    empleado = db.session.query(tPersona).filter_by(CURP=curp).first()
    if empleado is None:
        empleado = consultar_curp(curp)
        session["idPersona"] = None
        return jsonify(empleado)
    else:
        empleado_dict = empleado.__dict__
        empleado_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        session["idPersona"] = empleado_dict["idPersona"]

        return jsonify(empleado_dict)
    
@gestion_empleados.route('/rh/gestion-empleados/cargar-cp', methods = ['POST'])
def cargar_CP():
    Entidad  = request.form.get("Entidad")
    Municipio  = request.form.get("Municipio")
    TipoAsentamiento  = request.form.get("TipoAsentamiento")
    Asentamiento = request.form.get("Asentamiento")
    CPbusqueda = db.session.query(kCodigoPostal).filter_by(idEntidad = Entidad, idMunicipio = Municipio, idTipoAsentamiento = TipoAsentamiento, idAsentamiento = Asentamiento, Activo = 1).first()
    
    if CPbusqueda:
        codigo_postal = CPbusqueda.CodigoPostal
        return jsonify(codigo_postal)
    else:
        return "no encontrado"
    
@gestion_empleados.route('/rh/gestion-empleados/buscar-cp', methods = ['POST'])
def buscar_CP():
    CP = request.form.get("CP")
    CPbusqueda = db.session.query(kCodigoPostal).filter_by(CodigoPostal = CP, Activo = 1).first()
    if CPbusqueda:
        CPbusqueda = CPbusqueda.__dict__
        CPbusqueda.pop("_sa_instance_state", None)
        return jsonify(CPbusqueda)
    else:
        return "no encontrado"
    
@gestion_empleados.route('/rh/selecciona-empleado', methods = ['POST', 'GET'])
@permisos_de_consulta
def seleccionar_empleado():
    idSeleccionado = request.form.get("idSeleccionado")
    session['idPersona'] = idSeleccionado
    empleado = db.session.query(tPersona).filter_by(idPersona = idSeleccionado).first()
    if empleado is not None:
        empleado = empleado.__dict__
        empleado.pop("_sa_instance_state", None)
    return jsonify(empleado)