from flask import render_template, request, jsonify, current_app, send_from_directory, url_for
import openpyxl
import openpyxl.workbook
from datetime import datetime, date, time
import os
from dateutil.relativedelta import relativedelta

from .reportes import reportes
from app import db
from rh.gestion_empleados.modelos.empleado import rEmpleadoPuesto, rMovimientoEmpleado
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from general.herramientas.funciones import calcular_quincena

@reportes.route("/rh/reportes/por-movimientos", methods = ["POST", "GET"])
def por_movimientos():

    return render_template("/por_movimientos.html", title = "Por movimientos")

@reportes.route("/rh/reportes/generar_reporte_por_movimiento", methods = ["POST"])
def generar_reporte():
    movimiento = request.form.get("Movimiento")
    wb = openpyxl.Workbook()
    archivo_generado = None
    
    if movimiento == "1":
        altas = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idTipoMovimiento.in_([1, 2])).all()
        for empleado_alta in altas:
            empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_alta.idPersonaMod).first()
            domicilio = db.session.query(rDomicilio).filter_by(idPersona = empleado_alta.idPersonaMod, idTipoDomicilio = 1).first()
            if empleado:
                hoja = wb.active
                hoja["A1"] = "CONSTANCIA DE NOMBRAMIENTO"
                hoja["A2"] = "FOLIO"
                hoja["B2"] = empleado_alta.idMovimientoEmpleado
                hoja["A3"] = "FECHA DE ELABORACIÓN"
                hoja["B3"] = datetime.now().strftime("%d-%m-%Y")
                hoja["A4"] = "APELLIDO PATERNO"
                hoja["B4"] = empleado.Empleado.Persona.ApPaterno
                hoja["A5"] = "APELLIDO MATERNO"
                hoja["B5"] = empleado.Empleado.Persona.ApMaterno
                hoja["A6"] = "NOMBRE(S)"
                hoja["B6"] = empleado.Empleado.Persona.Nombre
                hoja["A7"] = "RFC"
                hoja["B7"] = empleado.Empleado.Persona.RFC
                hoja["A8"] = "CURP"
                hoja["B8"] = empleado.Empleado.Persona.CURP
                hoja["A9"] = "ESTADO CIVIL"
                hoja["B9"] = empleado.Empleado.Persona.idEstadoCivil # Hacer relación
                hoja["A10"] = "NACIONALIDAD"
                hoja["B10"] = empleado.Empleado.Persona.idNacionalidad # Hacer relación
                hoja["A11"] = "SEXO"
                hoja["B11"] = empleado.Empleado.Persona.Sexo
                hoja["A12"] = "EDAD"
                FechaNacimiento = empleado.Empleado.Persona.FechaNacimiento
                FechaNacimiento = datetime.combine(FechaNacimiento, time())
                FechaActual = datetime.today()
                edad = relativedelta(FechaActual, FechaNacimiento).years
                hoja["B12"] = edad
                hoja["A13"] = "CALLE Y No"
                hoja["B13"] = str(domicilio.Vialidad) + str(domicilio.NumExterior)
                hoja["A14"] = "COLONIA O POBLACIÓN"
                hoja["B14"] = domicilio.idAsentamiento # Hacer relación
                hoja["A15"] = "C.P."
                hoja["B15"] = domicilio.idCP
                hoja["A16"] = "ALCALDÍA O MUNICIPIO"
                hoja["B16"] = domicilio.idMunicipio # Hacer relación
                hoja["A17"] = "ENTIDAD FEDERATIVA"
                hoja["B17"] = domicilio.idEntidad # Hacer relación
                hoja["A18"] = "TELEFONO"
                hoja["B18"] = empleado.Empleado.Persona.TelCasa
                hoja["A19"] = "INGRESO A PLAZA"
                hoja["B19"] = ""
                hoja["A20"] = "TIPO DE NOMBRAMIENTO"
                hoja["B20"] = ""
                hoja["A21"] = "UNIDAD DE ADSCRIPCIÓN"
                hoja["B21"] = ""
                hoja["A22"] = "No PLAZA"
                hoja["B22"] = ""
                hoja["A23"] = "C.C."
                hoja["B23"] = empleado.Puesto.idCentroCosto # Hacer relación
                hoja["A24"] = "CLAVE PRESUPUESTAL"
                hoja["B24"] = empleado.Puesto.CodigoPresupuestal
                hoja["A25"] = "CÓDIGO PLAZA"
                hoja["B25"] = ""
                hoja["A26"] = "DENOMINACIÓN DEL PUESTO"
                hoja["B26"] = ""
                hoja["A27"] = "NIVEL"
                hoja["B27"] = empleado.Puesto.NivelSalarial
                hoja["A28"] = "RADICACIÓN"
                hoja["B28"] = ""
                hoja["A29"] = "FUNCIONES"
                hoja["B29"] = ""
                hoja["A30"] = "SUSTITUYE A"
                hoja["B30"] = ""
                hoja["A31"] = "RFC"
                hoja["B31"] = empleado.Empleado.Persona.RFC
                hoja["A32"] = "MOTIVO"
                hoja["B32"] = ""
                hoja["A33"] = "FECHA"
                hoja["B33"] = empleado.FechaInicio
                hoja["A34"] = "SUELDO BASE"
                hoja["B34"] = ""
                hoja["A35"] = "ESTIMULO AL PERSONAL"
                hoja["B35"] = ""
                hoja["A36"] = "COMP. GARANTIZADA"
                hoja["B36"] = ""
                hoja["A37"] = "TOTAL BRUTO"
                hoja["B37"] = ""
                hoja["A38"] = "JORNADA DE TRABAJO"
                hoja["B38"] = ""
                hoja["A39"] = "DEL"
                hoja["B39"] = ""
                hoja["A40"] = "HASTA"
                hoja["B40"] = ""
                hoja["A41"] = "OBSERVACIONES"
                hoja["B41"] = ""

                nombre_archivo = "alta_empleado_" + str(empleado.Empleado.NumeroEmpleado) + ".xlsx"

        if len(altas) > 0:
            respuesta = True
        else:
            respuesta = False

    if movimiento == "2":
        bajas = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idTipoMovimiento == 3).all()
        print(bajas)
        for empleado_baja in bajas:
            empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_baja.idPersonaMod).first()
            if empleado:
                hoja = wb.active
                hoja["A1"] = "AVISO BAJA Y/O CAMBIO DE SITUACIÓN DE PERSONAL FEDERAL"
                hoja["A2"] = "FOLIO"
                hoja["B2"] = empleado_baja.idMovimientoEmpleado
                hoja["A3"] = "APELLIDO PATERNO"
                hoja["B3"] = empleado.Empleado.Persona.ApPaterno
                hoja["A4"] = "APELLIDO MATERNO"
                hoja["B4"] = empleado.Empleado.Persona.ApMaterno
                hoja["A5"] = "NOMBRE(S)"
                hoja["B5"] = empleado.Empleado.Persona.Nombre
                hoja["A6"] = "RFC"
                hoja["B6"] = empleado.Empleado.Persona.RFC
                hoja["A7"] = "CLAVE PRESUPUESTAL"
                hoja["B7"] = empleado.Puesto.CodigoPresupuestal
                hoja["A8"] = "NIVEL"
                hoja["B8"] = empleado.Puesto.NivelSalarial
                hoja["A9"] = "CAUSA DE LA BAJA"
                hoja["B9"] = empleado.idCausaBaja
                hoja["A10"] = "No EMP"
                hoja["B10"] = empleado.Empleado.NumeroEmpleado
                hoja["A11"] = "C.C."
                hoja["B11"] = empleado.Puesto.idCentroCosto
                hoja["A12"] = "TIPO DE PLAZA"
                hoja["B12"] = ""
                hoja["A13"] = "CURP"
                hoja["B13"] = empleado.Empleado.Persona.CURP
                hoja["A14"] = "ADSCRIPCIÓN"
                hoja["B14"] = ""
                hoja["A15"] = "EFECTOS A PARTIR DE"
                hoja["B15"] = empleado.FechaEfecto
                

                nombre_archivo = "baja_empleado_" + str(empleado.Empleado.NumeroEmpleado) + ".xlsx"

        if len(bajas) > 0:
            respuesta = True
        else:
            respuesta = False

    if movimiento == "3":
        todos = db.session.query(rMovimientoEmpleado).all()
        cont = 1
        quincena = calcular_quincena()
        print(quincena)

        hoja = wb.active
        hoja["A1"] = "MOVIMIENTOS DEL PERSONAL DE PLAZA FEDERAL CORRESPONDIENTES A LA QUINCENA"
        hoja["A2"] = "Cons Qnal"
        hoja["B2"] = "No Qna"
        hoja["C2"] = "No Empleado"
        hoja["D2"] = "RFC"
        hoja["E2"] = "CURP"
        hoja["F2"] = "Nombre del Candidato"
        hoja["G2"] = "No Mov"
        hoja["H2"] = "Mov"
        hoja["I2"] = "Plaza"
        hoja["J2"] = "No Plaza"
        hoja["K2"] = "Nivel"
        hoja["L2"] = "CC Origen"
        hoja["M2"] = "Tipo Plaza"
        hoja["N2"] = "Puesto"
        hoja["O2"] = "Efectos a partir de"
        hoja["P2"] = "CC Propuesto"
        hoja["Q2"] = "Centro de Costo"
        hoja["R2"] = "Causa de la Baja"
        hoja["S2"] = "Grupo"
        hoja["T2"] = "Observaciones"
        
        for empleado_comb in todos:
            empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_comb.idPersonaMod).first()
            if empleado:
                hoja["A" + str(2 + cont)] = cont
                hoja["B" + str(2 + cont)] = str(datetime.now().year) +  str(quincena)
                hoja["C" + str(2 + cont)] = empleado.Empleado.NumeroEmpleado
                hoja["D" + str(2 + cont)] = empleado.Empleado.Persona.RFC
                hoja["E" + str(2 + cont)] = empleado.Empleado.Persona.CURP
                hoja["F" + str(2 + cont)] = empleado.Empleado.Persona.ApPaterno + " " + empleado.Empleado.Persona.ApMaterno + " " + empleado.Empleado.Persona.Nombre
                hoja["G" + str(2 + cont)] = empleado_comb.idMovimientoEmpleado
                hoja["H" + str(2 + cont)] = empleado_comb.idTipoMovimiento
                hoja["I" + str(2 + cont)] = ""
                hoja["J" + str(2 + cont)] = ""
                hoja["K" + str(2 + cont)] = empleado.Puesto.NivelSalarial
                hoja["L" + str(2 + cont)] = ""
                hoja["M" + str(2 + cont)] = ""
                hoja["N" + str(2 + cont)] = empleado.Puesto.Puesto
                hoja["O" + str(2 + cont)] = ""
                hoja["P" + str(2 + cont)] = ""
                hoja["Q" + str(2 + cont)] = empleado.Puesto.CentroCostos.CentroCosto
                hoja["R" + str(2 + cont)] = ""
                hoja["S" + str(2 + cont)] = ""
                hoja["T" + str(2 + cont)] = empleado.Observaciones
                cont = cont + 1

        nombre_archivo = "Reportes_Movimientos.xlsx"

        if len(todos) > 0:
            respuesta = True
        else:
            respuesta = False


    dir = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos")
    print(dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
        print("Directorio %s creado" % dir)
    else:
        print("Directorio %s ya existe" % dir)

    if respuesta:
        wb.save(dir + "/" + nombre_archivo)

        archivo_generado = nombre_archivo
    
    else:
        archivo_generado = ""

    return jsonify({"url_descarga": url_for("reportes.descargar_reporte", nombre_archivo=archivo_generado), "respuesta": respuesta})

@reportes.route("/rh/reportes/descargar-reporte/<nombre_archivo>")
def descargar_reporte(nombre_archivo):
    dir = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos")
    return send_from_directory(directory=dir, path=nombre_archivo, as_attachment=True)