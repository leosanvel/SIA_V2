from .rutas import consultas
from flask import request, jsonify, render_template
from flask_login import current_user

from sqlalchemy import and_, or_
from app import db
from autenticacion.modelos.modelos import User

from sqlalchemy.orm.exc import NoResultFound
from rh.gestion_asistencias.modelos.modelos import tChecador
from rh.gestion_empleados.modelos.empleado import rEmpleado

@consultas.route('/consultas/consulta-incidencias', methods=['POST', 'GET'])
def consulta_incidencias():
    return render_template('/consulta_incidencias.html', title='Consulta de incidencias',
                           current_user=current_user)


@consultas.route('/consultas/consultar-incidencia', methods = ['POST'])
def consultar_incidencia():
    idPersona = request.form.get('idPersona')
    BuscaFechaInicio = request.form.get('BuscaFechaInicioFormateada')
    BuscaFechaFin = request.form.get('BuscaFechaFinFormateada')

    query = db.session.query(tChecador)

    if idPersona:
        query = query.filter(tChecador.idPersona == int(idPersona))
    if BuscaFechaInicio and BuscaFechaFin:
        query = query.filter(and_(tChecador.Fecha >= BuscaFechaInicio, tChecador.Fecha <= BuscaFechaFin))
    elif BuscaFechaInicio:
        query = query.filter(tChecador.Fecha >= BuscaFechaInicio)
    elif BuscaFechaFin:
        query = query.filter(tChecador.Fecha <= BuscaFechaFin)

    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not (idPersona or BuscaFechaInicio or BuscaFechaFin):
        checadores = []
    else:
        checadores = query.filter(or_(tChecador.HoraEntrada == None, tChecador.HoraSalida == None, tChecador.idQuincenaReportada != None, tChecador.idIncidencia != None, tChecador.idJustificante != None))


    lista_checadores = []
    for checador in checadores:
        if checador is not None:
            try:
                empleado = db.session.query(rEmpleado).filter(rEmpleado.idPersona == checador.idPersona).one()
                checador_dict = checador.__dict__
                checador_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                checador_dict["NumeroEmpleado"] = empleado.NumeroEmpleado

                # Convertir los objetos datetime.date y datetime.time a cadenas
                checador_dict["Fecha"] = checador.Fecha.strftime("%Y-%m-%d")
                if checador.HoraEntrada:
                    checador_dict["HoraEntrada"] = checador.HoraEntrada.strftime("%H:%M:%S")
                if checador.HoraSalida:
                    checador_dict["HoraSalida"] = checador.HoraSalida.strftime("%H:%M:%S")


                lista_checadores.append(checador_dict)
            except NoResultFound:
                print("Empleado no encontrado")
    return jsonify(lista_checadores)
