from .gestion_asistencias import gestion_asistencias
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from datetime import datetime, time
import numpy as np

from app import db
from rh.gestion_asistencias.modelos.modelos import tJustificante, tChecador
from rh.gestion_tiempo_no_laboral.modelos.modelos import rDiasPersona
from rh.gestion_empleados.modelos.empleado import rEmpleado
from catalogos.modelos.modelos import kQuincena, kTipoProceso, kTipoJustificante, kPeriodoVacacional, rTipoProcesoJustificante

@gestion_asistencias.route('/rh/gestion-asistencias/justificantes', methods = ['POST', 'GET'])
def gestiona_justificantes():
    TipoProceso = db.session.query(kTipoProceso).filter_by(Activo = 1).all()
    periodovacacional = db.session.query(kPeriodoVacacional).all() 
    quincenas = db.session.query(kQuincena).all()
    return render_template('/justificantes.html', title='Justificantes',
                           current_user=current_user,
                           TipoProceso = TipoProceso,
                           PeriodoVacacional = periodovacacional,
                           quincenas = quincenas)

@gestion_asistencias.route('/cargar-tipo-justificante', methods = ['POST'])
def select_TipoJustificante():
    TipoProceso = request.form.get('TipoProceso')
    
    TipoJustificantes = db.session.query(kTipoJustificante).outerjoin(rTipoProcesoJustificante, kTipoJustificante.idTipoJustificante == rTipoProcesoJustificante.idTipoJustificante).filter(rTipoProcesoJustificante.idTipoProceso == TipoProceso, kTipoJustificante.Activo == 1).order_by(kTipoJustificante.TipoJustificante).all()     
    ret = '<option value="0">-- Seleccione --</option>'
    for entry in TipoJustificantes:
        ret += '<option value="{}">{}</option>'.format(entry.idTipoJustificante, entry.TipoJustificante)
    return ret

@gestion_asistencias.route('/rh/gestion-asistencias/guardar-justificante', methods = ['POST'])
def guarda_Justificante():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idJustificante' : 'idJustificante',
        'idPersona' : 'idPersona',
        'Descripcion' : 'Descripcion',
        'TipoJustificante' : 'idTipo',
        'FechaInicio' : 'FechaInicio',
        'FechaFin' : 'FechaFin'
    }
    justificante_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    fechasConsecutivas = request.form.get("checkFechasConsecutivas") # (True or None)

    if fechasConsecutivas:
        justificante_data['FechaInicio'] = datetime.strptime(justificante_data['FechaInicio'], '%d/%m/%Y')
        justificante_data['FechaFin'] = datetime.strptime(justificante_data['FechaFin'], '%d/%m/%Y')
        dias = np.busday_count(justificante_data["FechaInicio"].date(), justificante_data["FechaFin"].date(), weekmask='1111100')
        if(justificante_data["FechaFin"].weekday() < 5):
            dias = dias + 1
        guardar_o_modificar_justificante(justificante_data)
    else:
        FechasFlatpickr = request.form.get("FechasFlatpickr")
        fechas = FechasFlatpickr.split(',')  # Separa las fechas por comas
        dias = len(fechas)
        for fecha in fechas:
            fecha = fecha.strip()
            justificante_data['FechaInicio'] = datetime.strptime(fecha, '%d/%m/%Y')
            justificante_data['FechaFin'] = datetime.strptime(fecha, '%d/%m/%Y')
            guardar_o_modificar_justificante(justificante_data)

    if(int(justificante_data["idTipo"]) == 7):
        listadias = request.form.get("listaDias").split(',')
        listaperiodo = request.form.get("listaPeriodo").split(',')
        listafecha = request.form.get("listaFecha").split(',')
        restar_diaspersona(justificante_data["idPersona"], listadias, listaperiodo, listafecha, dias)

    return jsonify(justificante_data)

def guardar_o_modificar_justificante(justificante_data):
    nuevo_justificante = None

    try:
        justificante_a_modificar = db.session.query(tJustificante).filter(tJustificante.idJustificante == justificante_data["idJustificante"]).one()
       
        id_persona = justificante_a_modificar.idPersona

        checadores = db.session.query(tChecador).filter(
            tChecador.idPersona == id_persona,
            tChecador.Fecha >= justificante_a_modificar.FechaInicio,
            tChecador.Fecha <= justificante_a_modificar.FechaFin
        ).all()

        # Iterar sobre los registros y reiniciar info de incidencia
        for checador in checadores:
            checador.idJustificante = None
            if checador.idIncidencia == None:
                checador.HoraEntrada = time(9, 0, 0)
                checador.HoraSalida = time(18, 0, 0)
            else:    
                checador.HoraEntrada = None
                checador.HoraSalida = None

            
        # Actualizar los atributos de 'justificante_existente' con los valores de 'justificante_data'
        justificante_a_modificar.update(**justificante_data)
        # for attr, value in justificante_data.items():
        #     if not attr.startswith('_') and hasattr(justificante_a_modificar, attr):
        #         setattr(justificante_a_modificar, attr, value)
                
    except NoResultFound:
        if request.form.get('TipoProceso') == '2':
            numeros_empleados = db.session.query(rEmpleado.idPersona).filter_by(Activo = 1).all()
            # Extrae los números de empleado de la lista de tuplas
            numeros_empleados = [numero[0] for numero in numeros_empleados]
            for id_empleado in numeros_empleados:
                justificante_data['idPersona'] = int(id_empleado)
                nuevo_justificante = tJustificante(**justificante_data)
                # if (justificante_data["idTipo"] == 7):
                    # restar_diaspersona(int(id_empleado), fecha_inicio, fecha_fin)
                db.session.add(nuevo_justificante)

        elif(request.form.get('TipoProceso') == '1'): # Proceso individual
            nuevo_justificante = tJustificante(**justificante_data)
            # if (int(justificante_data["idTipo"]) == 7):
                # restar_diaspersona(int(justificante_data["idPersona"]), fecha_inicio, fecha_fin)
            db.session.add(nuevo_justificante)

    # Realizar cambios en la base de datos
    db.session.commit()

def restar_diaspersona(idPersona, listadias, listaperiodo, listafecha, dias):
    for indice, tupla in enumerate(zip(listadias, listaperiodo, listafecha)):
        try:
            DiasPersonas_existente = db.session.query(rDiasPersona).filter_by(idPersona = idPersona, idPeriodo = listaperiodo[indice], DiasGanados = listadias[indice], Fecha = datetime.strptime(listafecha[indice], '%d/%m/%Y')).one()
            print(DiasPersonas_existente)

        #     for DiasPersona in DiasPersonas_existente:
            if(dias == 0):
                break

            if(DiasPersonas_existente.DiasGanados >= dias):
                DiasPersonas_existente.DiasGanados = DiasPersonas_existente.DiasGanados - dias
                dias = 0
            else:
                dias = dias - DiasPersonas_existente.DiasGanados
                DiasPersonas_existente.DiasGanados = 0

            print("dias = ", dias)
            print(DiasPersonas_existente.DiasGanados)
        #         if(DiasPersona.DiasGanados != 0):
        #             if(DiasPersona.DiasGanados >= dias):
        #                 DiasPersona.DiasGanados = DiasPersona.DiasGanados - dias
        #                 dias = 0
        #             else:
        #                 dias = dias - DiasPersona.DiasGanados
        #                 DiasPersona.DiasGanados = 0

            correcto = True

        except NoResultFound:
            correcto = False
        
    db.session.commit()
    return correcto


@gestion_asistencias.route('/rh/gestion-asistencias/buscar-justificante', methods = ['POST'])
def busca_Justificante():
    idPersona = request.form.get('idPersona')
    
    BuscaFechaInicio = request.form.get('BuscaFechaInicioFormateada')
    BuscaFechaFin = request.form.get('BuscaFechaFinFormateada')

    query = db.session.query(tJustificante)

    if idPersona:
        query = query.filter(tJustificante.idPersona == int(idPersona))
    if BuscaFechaInicio and BuscaFechaFin:
        query = query.filter(and_(tJustificante.FechaInicio >= BuscaFechaInicio, tJustificante.FechaInicio <= BuscaFechaFin))
    elif BuscaFechaInicio:
        query = query.filter(tJustificante.FechaInicio >= BuscaFechaInicio)
    elif BuscaFechaFin:
        query = query.filter(tJustificante.FechaInicio <= BuscaFechaFin)
    
    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not (idPersona or BuscaFechaInicio or BuscaFechaFin):
        justificantes = []
    else:
        justificantes = query.all()

    lista_justificantes = []
    for justificante in justificantes:
        if justificante is not None:
            try:
                empleado = db.session.query(rEmpleado).filter(rEmpleado.idPersona == justificante.idPersona, rEmpleado.Activo == 1).one()

            except NoResultFound:
                print("Empleado no encontrado")

            justificante_dict = justificante.__dict__
            justificante_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            justificante_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
            lista_justificantes.append(justificante_dict)

    return jsonify(lista_justificantes)

@gestion_asistencias.route('/rh/gestion-asistencias/eliminar-justificante', methods = ['POST'])
def eliminar_Justificante():
    idJustificante = request.form.get("idJustificante")
    try:
        Justificante = db.session.query(tJustificante).get(idJustificante)

        db.session.delete(Justificante)

        db.session.commit()

    except NoResultFound:
        print("No se encontró justificante")

    return jsonify({"eliminado": True})

@gestion_asistencias.route('/rh/gestion-asistencias/cancela-justificante', methods = ['POST', 'GET'])
def cancela_justificante():
    idJustificante = request.form.get('idJustificante')
    justificante = db.session.query(tJustificante).filter_by(idJustificante = idJustificante).first()
    if justificante is not None:
        justificante_dict = justificante.__dict__
        justificante_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(justificante_dict)
    else:
        return jsonify(False)