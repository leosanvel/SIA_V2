from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory, url_for
from sqlalchemy import desc, or_, and_, inspect
import os

from app import db
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *

@gestion_empleados.route('/rh/gestion-empleados/crear-contrato', methods = ['POST', 'GET'])
def crear_contrato():
    Entidad = db.session.query(kEntidad).filter_by(Activo=1).order_by(kEntidad.Entidad).all()    
    Municipio = db.session.query(kMunicipio).filter_by(idEntidad = 9, Activo=1).order_by(kMunicipio.Municipio).all()
    return render_template('/crear_contrato.html', title = 'Crear contrato',
                           Entidad = Entidad,
                           Municipio = Municipio)

@gestion_empleados.route('/rh/gestion-empleados/validar_empleado_contrato', methods = ['POST', 'GET'])
def validar_empleado_contrato():
    respuesta = 0
    strAnios = ""
    Conocimiento = ""
    Sueldo = ""
    datos_contrato = {}
    NumeroContrato = request.form.get("NumeroContrato")
    EmpleadoContrato_dict = None
    Empleado = db.session.query(rEmpleado).filter_by(NumeroEmpleado = request.form.get("NumeroBuscarEmpleado")).first()
    print(Empleado)
    if Empleado:
        if Empleado.Activo == 1:
            if Empleado.idTipoEmpleado == 1:
                respuesta = 99
                Puesto =  db.session.query(rEmpleadoPuesto).filter_by(idPersona = Empleado.idPersona).first()
                if Puesto:
                    CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = Puesto.idCentroCosto).first()
                    if CentroCosto:
                        PuestoHonorarios = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = Puesto.idPuesto).first()
                        if PuestoHonorarios:
                            EmpleadoContrato = db.session.query(rEmpleadoContrato).filter_by(idPersona = Empleado.idPersona, NumeroContrato = NumeroContrato).first()
                            if EmpleadoContrato:
                                EmpleadoContrato_dict = EmpleadoContrato.__dict__
                                EmpleadoContrato_dict.pop("_sa_instance_state", None)
                                Sueldo = PuestoHonorarios.SueldoMensual
                                if PuestoHonorarios.Nivel == "O33":
                                    strAnios = "2"
                                else:
                                    strAnios = "4"
                                Conocimiento = "APOYO EN MATERIA "+str(CentroCosto.Materia)+" Y EXPERIENCIA DE " + strAnios + " AÑOS PARA CUMPLIR CON EL OBJETO DEL CONTRATO, CON BASE A LAS ACTIVIDADES A DESARROLLAR ESTABLECIDAS EN LA CLÁUSULA PRIMERA DEL CONTRATO DE PRESTACIÓN DE SERVICIOS CELEBRADO POR ESTE ÓRGANO DESCONCENTRADO CON ESTUDIOS DE MAESTRO EN CIENCIAS EN COMPUTACION"
            else:
                respuesta = 2
        else:
            respuesta = 1

    return jsonify({"respuesta":respuesta,"DatosContrato": EmpleadoContrato_dict})

@gestion_empleados.route('/rh/gestion-empleados/buscar-empleado-contrato', methods = ['POST', 'GET'])
def buscar_empleados_contrato():
    respuesta = 0
    idPersona = request.form.get("idPersona")
    print(idPersona)

    EmpleadoPuesto = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona).order_by(desc(rEmpleadoPuesto.FechaInicio)).first()
    if EmpleadoPuesto.idEstatusEP == 1:

            if EmpleadoPuesto.Empleado.idTipoEmpleado == 1:
                respuesta = 99
                CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = EmpleadoPuesto.idCentroCosto).first()
                if CentroCosto:
                    Puesto = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = EmpleadoPuesto.idPuesto).first()
                    if Puesto:
                        if Puesto.Nivel == "O33":
                            strAnios = "2"
                        else:
                            strAnios = "4"
                        Conocimiento = "APOYO EN MATERIA "+ str(CentroCosto.Materia)+ " Y EXPERIENCIA DE " + strAnios + " AÑOS PARA CUMPLIR CON EL OBJETO DEL CONTRATO, CON BASE A LAS ACTIVIDADES A DESARROLLAR ESTABLECIDAS EN LA CLÁUSULA PRIMERA DEL CONTRATO DE PRESTACIÓN DE SERVICIOS CELEBRADO POR ESTE ÓRGANO DESCONCENTRADO CON ESTUDIOS DE MAESTRO EN CIENCIAS EN COMPUTACION"
                        print(Conocimiento)
            else:
                respuesta = 2
    else:
        respuesta = 1

    print(respuesta)

    return jsonify({"respuesta": respuesta, "Conocimiento": Conocimiento})
    


@gestion_empleados.route('/rh/gestion-empleados/guardar_empleado_contrato', methods = ['POST', 'GET'])
def guardar_empleado_contrato():
    respuesta = 0

    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona': 'idPersona',
        'FechaInicio': 'FechaInicio',
        'FechaFin': 'FechaFin',
        'FechaFirma': 'FechaFirma',
        'Estado': 'idEstado',
        'Municipio': 'idMunicipio',
        'ConocimientoExperiencia': 'ConocimientoExperiencia',
        'ImporteBruto': 'ImporteBruto',
        'NumeroExhibiciones': 'NumeroExhibicion',
        'MontoPactado': 'MontoPactado',
        'Proyecto': 'Proyecto',
        'Partida': 'Partida',
        'Origen': 'Origen',
        'ConocimientoPrestador': 'ConocimientoPrestador',
        'OficioDictamen': 'OficioDictamen',
        'Actividades': 'Actividades',
        'CURPEntregable': 'CURPEntrega',
        'CURPFirma': 'CURPFirma'
    }
    idPersona = request.form.get("idPersona")
    
    # FechaInicio = request.form.get("FechaInicio")
    # FechaInicio = datetime.strptime(FechaInicio, '%d/%m/%Y')
    # FechaFin = request.form.get("FechaFin")
    # FechaFin = datetime.strptime(FechaFin, '%d/%m/%Y')
    # FechaFirma = request.form.get("FechaFirma")
    # FechaFirma = datetime.strptime(FechaFirma, '%d/%m/%Y')
    # idEstado = request.form.get("Estado")
    # idMunicipio = request.form.get("Municipio")
    # ConocimientoExperiencia = request.form.get("ConocimientoExperiencia")
    # ImporteBruto = request.form.get("ImporteBruto")
    # NumeroExhibicion = request.form.get("NumeroExhibiciones")
    # MontoPactado = request.form.get("MontoPactado")
    # Proyecto = request.form.get("Proyecto")
    # Partida = request.form.get("Partida")
    # Origen = request.form.get("Origen")
    # ConocimientoPrestador = request.form.get("ConocimientoPrestador")
    # OficioDictamen = request.form.get("OficioDictamen")
    # Actividades = request.form.get("Actividades")
    # CURPEntrega = request.form.get("CURPEntregable")
    # CURPFirma = request.form.get("CURPFirma")

    Contrato_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    Contrato_data["FechaInicio"] = datetime.strptime(Contrato_data["FechaInicio"], '%d/%m/%Y')
    Contrato_data["FechaFin"] = datetime.strptime(Contrato_data["FechaFin"], '%d/%m/%Y')
    Contrato_data["FechaFirma"] = datetime.strptime(Contrato_data["FechaFirma"], '%d/%m/%Y')
    Contrato_data["AnioFiscal"] = Contrato_data["FechaInicio"].year
    Contrato_data["OficioDGHO"] = ""
    print(Contrato_data)

    Datos_contrato_existente = db.session.query(rEmpleadoContrato).filter(
        rEmpleadoContrato.idPersona == Contrato_data["idPersona"],
        or_(
            and_(
                rEmpleadoContrato.FechaInicio <= Contrato_data["FechaInicio"],
                rEmpleadoContrato.FechaFin >= Contrato_data["FechaInicio"]
            ),
            and_(
                rEmpleadoContrato.FechaInicio <= Contrato_data["FechaFin"],
                rEmpleadoContrato.FechaFin >= Contrato_data["FechaFin"]
            ),
            and_(
                rEmpleadoContrato.FechaInicio >= Contrato_data["FechaInicio"],
                rEmpleadoContrato.FechaFin <= Contrato_data["FechaFin"]
            )
        )
    ).first()

    print(Datos_contrato_existente)

    if Datos_contrato_existente is None:
        ultimo_NumeroContrato = db.session.query(func.max(rEmpleadoContrato.NumeroContrato)).filter_by(idPersona = Contrato_data["idPersona"]).scalar()
        if ultimo_NumeroContrato is None:
            Contrato_data["NumeroContrato"] = 1
        else:
            Contrato_data["NumeroContrato"] = ultimo_NumeroContrato + 1

        Contrato_data["ContratoGenerado"] = 0

        nuevo_contrato = rEmpleadoContrato(**Contrato_data)
        db.session.add(nuevo_contrato)
        db.session.commit()

        estado = inspect(nuevo_contrato)
        if estado.persistent:
            respuesta = 99
        else:
            respuesta = 2
        
    else:
        respuesta = 1


    return jsonify({"respuesta":respuesta})
