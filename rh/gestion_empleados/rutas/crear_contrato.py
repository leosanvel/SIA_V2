from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory

import os

from app import db
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *

@gestion_empleados.route('/rh/gestion-empleados/crear-contrato', methods = ['POST', 'GET'])
def crear_contrato():
    Entidad = db.session.query(kEntidad).filter_by(Activo=1).order_by(kEntidad.Entidad).all()    
    Municipio = db.session.query(kMunicipio).filter_by(idEntidad = 9, Activo=1).order_by(kMunicipio.Municipio).all()
    return render_template('/crear_contrato.html', title = 'Crear contrato', Entidad = Entidad,Municipio = Municipio)

@gestion_empleados.route('/rh/gestion-empleados/validar_empleado_contrato', methods = ['POST', 'GET'])
def validar_empleado_contrato():
    respuesta = 0
    strAnios = ""
    Conocimiento = ""
    Sueldo = ""
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

    return jsonify({"respuesta":respuesta,"conocimiento":Conocimiento,"sueldo":Sueldo})

@gestion_empleados.route('/rh/gestion-empleados/guardar_empleado_contrato', methods = ['POST', 'GET'])
def guardar_empleado_contrato():
    respuesta = 0
    
    idPersona = 1
    NumeroContrato = 1
    FechaInicio = request.form.get("FechaInicio")
    FechaFin = request.form.get("FechaFin")
    FechaFirma = request.form.get("FechaFirma")
    idEstado = request.form.get("Estado")
    idMunicipio = request.form.get("Municipio")
    ConocimientoExperiencia = request.form.get("ConocimientoExperiencia")
    ImporteBruto = request.form.get("ImporteBruto")
    NumeroExhibicion = request.form.get("NumeroExhibiciones")
    MontoPactado = request.form.get("MontoPactado")
    Proyecto = request.form.get("Proyecto")
    Partida = request.form.get("Partida")
    Origen = request.form.get("Origen")
    ConocimientoPrestador = request.form.get("ConocimientoPrestador")
    OficioDictamen = request.form.get("OficioDictamen")
    Actividades = request.form.get("Actividades")
    CURPEntrega = request.form.get("CURPEntregable")
    CURPFirma = request.form.get("CURPFirma")

    nuevo_contrato = rEmpleadoContrato(idPersona = idPersona,
                                        NumeroContrato = NumeroContrato,
                                        FechaInicio = FechaInicio,
                                        FechaFin = FechaFin,
                                        FechaFirma = FechaFirma,
                                        idEstado = idEstado,
                                        idMunicipio = idMunicipio,
                                        ImporteBruto = ImporteBruto,
                                        NumeroExhibicion = NumeroExhibicion,
                                        MontoPactado = MontoPactado,
                                        Proyecto = Proyecto,
                                        Partida = Partida,
                                        Origen = Origen,
                                        ConocimientoPrestador = ConocimientoPrestador,
                                        OficioDictamen = OficioDictamen,
                                        OficioDGHO = "",
                                        ConocimientoExperiencia = ConocimientoExperiencia,
                                        Actividades = Actividades,
                                        CURPEntrega = CURPEntrega,
                                        CURPFirma = CURPFirma)
    db.session.add(nuevo_contrato)
    db.session.commit()


    return jsonify({"respuesta":respuesta})
