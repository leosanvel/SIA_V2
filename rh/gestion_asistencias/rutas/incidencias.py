from .gestion_asistencias import gestion_asistencias
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_,func
from datetime import datetime, time, timedelta

from app import db
from catalogos.modelos.modelos import kQuincena, kTipoIncidencia, kPeriodoVacacional
from rh.gestion_asistencias.modelos.modelos import rPoliticaPersona, tIncidencia, tChecador
from rh.gestion_empleados.modelos.empleado import rEmpleado
from general.modelos.modelos import tBitacora
from general.herramientas.funciones import calcular_quincena

@gestion_asistencias.route('/rh/gestion-asistencias/incidencias', methods = ['POST', 'GET'])
def gestiona_incidencias():

    periodovacacional = db.session.query(kPeriodoVacacional).all() 
    quincenas = db.session.query(kQuincena).all()
    return render_template('/incidencias.html', title='Incidencias',
                           current_user=current_user,
                           PeriodoVacacional = periodovacacional,
                           quincenas = quincenas)


@gestion_asistencias.route('/cargar-tipo-incidencia', methods = ['POST'])
def select_TipoIncidencia():
    
    TipoIncidencias = db.session.query(kTipoIncidencia).filter(kTipoIncidencia.Activo == 1).order_by(kTipoIncidencia.TipoIncidencia).all()     
    ret = '<option value="0">-- Seleccione --</option>'
    for entry in TipoIncidencias:
        ret += '<option value="{}">{}</option>'.format(entry.idTipoIncidencia, entry.TipoIncidencia)
    return ret



@gestion_asistencias.route('/rh/gestion-asistencias/guardar-incidencia', methods = ['POST'])
def guarda_Incidencia():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idIncidencia' : 'idIncidencia',
        'idPersona' : 'idPersona',
        'Descripcion' : 'Descripcion',
        'TipoIncidencia' : 'idTipo',
        'fechaInicio' : 'FechaInicio',
        'fechaFin' : 'FechaFin',
    }

    incidencia_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    idPersona = incidencia_data.get(mapeo_nombres["idPersona"],None)
    idIncidencia = incidencia_data.get(mapeo_nombres["idIncidencia"],None)
    TipoIncidencia = int(incidencia_data.get(mapeo_nombres["TipoIncidencia"],None))
    
    fechasConsecutivas = request.form.get("checkFechasConsecutivas") # (True or None)

    falta = False
    entrada = False
    salida = False
    if TipoIncidencia == 1:
        politica = db.session.query(rPoliticaPersona).filter(rPoliticaPersona.idPolitica.in_([1]), rPoliticaPersona.idPersona == idPersona).all()
        if politica:
            falta = True
    if TipoIncidencia == 2:
        politica = db.session.query(rPoliticaPersona).filter(rPoliticaPersona.idPolitica.in_([2,3]), rPoliticaPersona.idPersona == idPersona).all()
        if politica:
            entrada = True
    if TipoIncidencia == 6:
        politica = db.session.query(rPoliticaPersona).filter(rPoliticaPersona.idPolitica.in_([4,5]), rPoliticaPersona.idPersona == idPersona).all()
        if politica:
            salida = True
    
    if (falta or entrada or salida):
        
        if fechasConsecutivas:
            incidencia_data['FechaInicio'] = datetime.strptime(incidencia_data['FechaInicio'], '%d/%m/%Y')
            incidencia_data['FechaFin'] = datetime.strptime(incidencia_data['FechaFin'], '%d/%m/%Y')
            # incidencias_pasadas(incidencia_data)
            guardar_o_modificar_incidencia(incidencia_data)
        else:
            FechasFlatpickr = request.form.get("FechasFlatpickr")
            fechas = FechasFlatpickr.split(',')  # Separa las fechas por comas
            for fecha in fechas:
                fecha = fecha.strip()
                incidencia_data['FechaInicio'] = datetime.strptime(fecha, '%d/%m/%Y')
                incidencia_data['FechaFin'] = datetime.strptime(fecha, '%d/%m/%Y')
                # incidencias_pasadas(incidencia_data)
                guardar_o_modificar_incidencia(incidencia_data)
        return jsonify(incidencia_data)
    else:
        return jsonify({"error":"El empleado no tiene la politica"})
    
def guardar_o_modificar_incidencia(incidencia_data):
    nuevo_incidencia = None
    try:
        incidencia_a_modificar = db.session.query(tIncidencia).filter(tIncidencia.idIncidencia == incidencia_data["idIncidencia"]).one()
        id_persona = incidencia_a_modificar.idPersona

        checadores = db.session.query(tChecador).filter(
            tChecador.idPersona == id_persona,
            tChecador.Fecha >= incidencia_a_modificar.FechaInicio,
            tChecador.Fecha <= incidencia_a_modificar.FechaFin
        ).all()

        # Iterar sobre los registros y recuperar horas (cancelar la incidencia a modificar)
        for checador in checadores:
            checador.HoraEntrada = time(9, 0, 0)
            checador.HoraSalida = time(18, 0, 0)
            checador.idIncidencia = None

        # Actualizar los atributos de 'incidencia_a_modificar' con los valores de 'justificante_data'
        for attr, value in incidencia_data.items():
            if not attr.startswith('_') and hasattr(incidencia_a_modificar, attr):
                setattr(incidencia_a_modificar, attr, value)

        crear_modificar_incidencia = 8
                
    except NoResultFound:

        checadores = db.session.query(tChecador).filter(
            tChecador.idPersona == incidencia_data["idPersona"],
            tChecador.Fecha >= incidencia_data['FechaInicio'],
            tChecador.Fecha <= incidencia_data['FechaFin'],
        ).all()


        ultimo_idIncidencia = db.session.query(func.max(tIncidencia.idIncidencia)).scalar()
        if ultimo_idIncidencia:
            idIncidencia = ultimo_idIncidencia + 1
        else:
            idIncidencia = 1
        incidencia_data["idIncidencia"] = idIncidencia

        # Iterar sobre los registros y actualizar según el tipo de incidencia o justificante
        for checador in checadores:
            if (checador.idJustificante == None):
                checador.idIncidencia = idIncidencia
                if incidencia_data["idTipo"] == "1":
                    checador.HoraEntrada = None
                    checador.HoraSalida = None
                if incidencia_data["idTipo"] == "2":
                    checador.HoraEntrada = None
                if incidencia_data["idTipo"] == "6":
                    checador.HoraSalida = None
        nuevo_incidencia = tIncidencia(**incidencia_data)
        db.session.add(nuevo_incidencia)

        crear_modificar_incidencia = 7

    ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
    if ultimo_idBitacora is None:
        idBitacora = 1
    else:
        idBitacora = ultimo_idBitacora + 1

    nueva_bitacora = tBitacora(idBitacora=idBitacora,
                               idTipoMovimiento=crear_modificar_incidencia,
                               idUsuario=current_user.idPersona)
    
    db.session.add(nueva_bitacora)

    # Realizar cambios en la base de datos
    db.session.commit()

@gestion_asistencias.route('/rh/gestion-asistencias/buscar-incidencia', methods = ['POST'])
def busca_Incidencia():
    idPersona = request.form.get('idPersona')
    BuscaFechaInicio = request.form.get('BuscaFechaInicioFormateada')
    BuscaFechaFin = request.form.get('BuscaFechaFinFormateada')

    query = db.session.query(tIncidencia)

    if idPersona:
        query = query.filter(tIncidencia.idPersona == int(idPersona))
    if BuscaFechaInicio and BuscaFechaFin:
        query = query.filter(and_(tIncidencia.FechaInicio >= BuscaFechaInicio, tIncidencia.FechaInicio <= BuscaFechaFin))
    elif BuscaFechaInicio:
        query = query.filter(tIncidencia.FechaInicio >= BuscaFechaInicio)
    elif BuscaFechaFin:
        query = query.filter(tIncidencia.FechaInicio <= BuscaFechaFin)

    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not (idPersona or BuscaFechaInicio or BuscaFechaFin):
        incidencias = []
    else:
        incidencias = query.all()


    lista_incidencias = []
    for incidencia in incidencias:
        if incidencia is not None:
            try:
                empleado = db.session.query(rEmpleado).filter(rEmpleado.idPersona == incidencia.idPersona, rEmpleado.Activo == 1).one()
                incidencia_dict = incidencia.__dict__
                incidencia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                incidencia_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
                lista_incidencias.append(incidencia_dict)

            except NoResultFound:
                print("Empleado no encontrado, la persona no está activa")
    return jsonify(lista_incidencias)

@gestion_asistencias.route('/rh/gestion-asistencias/eliminar-incidencia', methods = ['POST'])
def eliminar_incidencia():
    idIncidencia = request.form.get("idIncidencia")
    try:
        Incidencia = db.session.query(tIncidencia).get(idIncidencia)
        print("Eliminando")
        id_persona = Incidencia.idPersona
        fecha_inicio = Incidencia.FechaInicio
        fecha_fin = Incidencia.FechaFin

    # Obtener registros de Tchecador para la persona y el rango de fechas
        checadores = db.session.query(tChecador).filter(
            tChecador.idPersona == id_persona,
            tChecador.Fecha >= fecha_inicio,
            tChecador.Fecha <= fecha_fin
        ).all()

        # Iterar sobre los registros y actualizar según el tipo de incidencia o justificante
        for checador in checadores:
            checador.HoraEntrada = time(9, 0, 0)
            checador.HoraSalida = time(18, 0, 0)
            
        db.session.delete(Incidencia)

        ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
        if ultimo_idBitacora is None:
            idBitacora = 1
        else:
            idBitacora = ultimo_idBitacora + 1

        nueva_bitacora = tBitacora(idBitacora=idBitacora,
                                   idTipoMovimiento=9,
                                   idUsuario=current_user.idPersona)
        db.session.add(nueva_bitacora)

        db.session.commit()

    except NoResultFound:
        print("No se encontró incidencia")

    return jsonify({"eliminado": True})
    
@gestion_asistencias.route('/RH/buscaFechasQuincena', methods = ['POST'])
def buscar_fechasquincenas():
    idQuincena = request.form.get("NumeroQuincena")

    if(idQuincena):
        try:
            Quincena = db.session.query(kQuincena).filter_by(idQuincena = idQuincena).one()
            Quincena_dict = Quincena.__dict__
            Quincena_dict.pop("_sa_instance_state", None)
            return jsonify(Quincena_dict)

        except NoResultFound:
            print("No hay quincena válida")
            return None
        

@gestion_asistencias.route('/rh/gestion-asistencias/cancelar-incidencia', methods = ['POST', 'GET'])
def cancela_incidencia():
    idIncidencia = request.form.get('idIncidencia')
    Incidencia = db.session.query(tIncidencia).filter_by(idIncidencia = idIncidencia).first()
    if Incidencia is not None:
        Incidencia_dict = Incidencia.__dict__
        Incidencia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(Incidencia_dict)
    else:
        return jsonify(False)
    
# def incidencias_pasadas(datos_incidencia):
#     print(datos_incidencia)
#     if datos_incidencia["FechaInicio"] == datos_incidencia["FechaFin"]:
#         incidencia_pasada_datos = {"idIncidenciaPasada": None,
#                                    "idPersona": datos_incidencia["idPersona"],
#                                    "Fecha": datos_incidencia["FechaInicio"],
#                                    "idQuincena": None,
#                                    "Activo": 1}
#         if datos_incidencia["FechaInicio"].weekday() < 5:
#             guardar_incidencias_pasadas(incidencia_pasada_datos)

#     else:
#         fecha = datos_incidencia["FechaInicio"]
#         while fecha <= datos_incidencia["FechaFin"]:
#             incidencia_pasada_datos = {"idIncidenciaPasada": None,
#                                        "idPersona": datos_incidencia["idPersona"],
#                                        "Fecha": fecha,
#                                        "idQuincena": None,
#                                        "Activo": 1}
            
#             if fecha.weekday() < 5:
#                 guardar_incidencias_pasadas(incidencia_pasada_datos)
            
#             fecha += timedelta(days=1)

# def guardar_incidencias_pasadas(datos_incidencia_pasada):
#     incidencias = db.session.query(tIncidenciasPasadas).filter_by(idPersona = datos_incidencia_pasada["idPersona"], Activo = 1).order_by(tIncidenciasPasadas.idQuincena.asc()).all()

#     if len(incidencias) >= 3:
#         tam = len(incidencias)
#         aux = tam//3
#         datos_incidencia_pasada["idQuincena"] = incidencias[0].idQuincena + aux

#     else:
#         datos_incidencia_pasada["idQuincena"] = calcular_quincena(datos_incidencia_pasada["Fecha"])

#     idIncidenciaPasada_existente = db.session.query(func.max(tIncidenciasPasadas.idIncidenciaPasada)).scalar()

#     if idIncidenciaPasada_existente is None:
#         idIncidenciaPasada = 1
#     else:
#         idIncidenciaPasada = idIncidenciaPasada_existente + 1

#     datos_incidencia_pasada["idIncidenciaPasada"] = idIncidenciaPasada

#     incidencia_pasada_nuevo = tIncidenciasPasadas(**datos_incidencia_pasada)

#     db.session.add(incidencia_pasada_nuevo)
#     db.session.commit()