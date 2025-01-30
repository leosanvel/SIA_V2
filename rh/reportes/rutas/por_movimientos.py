from flask import render_template, request, jsonify, current_app, send_from_directory, url_for
import openpyxl
import openpyxl.workbook
from datetime import datetime, date, time
import os
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
import zipfile
from io import BytesIO
import xlwings as xw

from .reportes import reportes
from app import db
from rh.gestion_empleados.modelos.empleado import rEmpleadoPuesto, rMovimientoEmpleado, tPuestoHonorarios
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from catalogos.modelos.modelos import kCentroCostos, kQuincena, kTipoEmpleado, kAnioFiscal, kEntidad, kMunicipio
from general.herramientas.funciones import calcular_quincena

@reportes.route("/rh/reportes/por-movimientos", methods = ["POST", "GET"])
def por_movimientos():
    Periodos = db.session.query(kAnioFiscal).all()
    #Quincenas = db.session.query(kQuincena).filter(func.extract('year', kQuincena.FechaInicio) == ).all()
    TipoEmpleado = db.session.query(kTipoEmpleado).filter_by(Activo = 1).all()

    return render_template("/por_movimientos.html", title = "Por movimientos",
                           Periodos = Periodos,
                           TipoEmpleado = TipoEmpleado)

@reportes.route("/rh/reportes/por-movimientos/obtener-quincenas", methods = ["POST"])
def obtener_quincenas():
    AnioFiscal = request.form.get("AnioFiscal")
    lista_quincenas = []

    Quincenas = db.session.query(kQuincena).filter(func.extract('year', kQuincena.FechaInicio) == int(AnioFiscal)).all()

    for Quincena in Quincenas:
        if Quincena is not None:
            Quincena_dict = Quincena.__dict__
            Quincena_dict.pop("_sa_instance_state", None)
            lista_quincenas.append(Quincena_dict)

    return jsonify(lista_quincenas)

@reportes.route("/rh/reportes/generar_reporte_por_movimiento", methods = ["POST"])
def generar_reporte():
    movimiento = request.form.get("Movimiento")
    quincena = request.form.get("Quincena")
    TipoEmpleado = request.form.get("TipoEmpleado")
    idPersona = request.form.get("idPersona")
    Periodo = request.form.get("Periodo")

    respuesta = True
    lista_archivos = []

    wb = openpyxl.Workbook()
    archivo_generado = None
    datos_a_escribir = {}

    dir = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos")
    if not os.path.exists(dir):
        os.mkdir(dir)
        print("Directorio %s creado" % dir)
    else:
        print("Directorio %s ya existe" % dir)

    lista_empleados = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idQuincena == quincena, rMovimientoEmpleado.idTipoEmpleado == TipoEmpleado)

    if idPersona != "":
        lista_empleados.filter(rMovimientoEmpleado.idPersonaMod == idPersona)
    
    if movimiento == "1":
        lista_empleados = lista_empleados.filter(rMovimientoEmpleado.idTipoMovimiento == 1).all()

        print(lista_empleados)
        #empleado_alta = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idTipoMovimiento.in_([1, 2]), rMovimientoEmpleado.idQuincena == quincena, rMovimientoEmpleado.idTipoEmpleado == TipoEmpleado, rMovimientoEmpleado.idPersonaMod == idPersona).first()
        #print(empleado_alta)
        #empleado_alta = None
        for empleado_alta in lista_empleados:
            if empleado_alta:
                empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_alta.idPersonaMod).order_by(rEmpleadoPuesto.FechaInicio.desc()).first()
                domicilio = db.session.query(rDomicilio).filter_by(idPersona = empleado_alta.idPersonaMod, idTipoDomicilio = 1).first()

                nombre_archivo = "Nombramiento_" + str(empleado.Empleado.NumeroEmpleado)+ '_' + str(quincena) + ".xlsx"
                nombre_archivo_pdf = "Nombramiento_" + str(empleado.Empleado.NumeroEmpleado)+ '_' + str(quincena) + ".pdf"
                ruta_pdf = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos", nombre_archivo_pdf)

                if not os.path.isfile("rh/reportes/archivos/movimientos/" + nombre_archivo):
                    print("El archivo no existe")

                    excel_app = xw.App(visible=False)
                    #ws = openpyxl.load_workbook(filename="rh/reportes/archivos/PLANTILLA NOMBRAMIENTO ADMINISTRATIVO.xlsx")
                    #plantilla = ws.active
                    wb = xw.Book("rh/reportes/archivos/PLANTILLA NOMBRAMIENTO ADMINISTRATIVO.xlsx")
                    plantilla = wb.sheets[0]
                    respuesta = True
    
                    if empleado:
                        TipoEmpleado = empleado.Empleado.idTipoEmpleado
                        #hoja = wb.active
                        datos_a_escribir["FOLIO_D"] = empleado_alta.idMovimientoEmpleado
                        datos_a_escribir["FECHA_D"] = datetime.now().strftime("%d-%m-%Y")
                        datos_a_escribir["APPATERNO_D"] = empleado.Empleado.Persona.ApPaterno
                        datos_a_escribir["APMATERNO_D"] = empleado.Empleado.Persona.ApMaterno
                        datos_a_escribir["NOMBRE_D"] = empleado.Empleado.Persona.Nombre
                        datos_a_escribir["RFC_D"] = empleado.Empleado.Persona.RFC if not None else ""
                        datos_a_escribir["CURP_D"] = empleado.Empleado.Persona.CURP
                        if empleado.Empleado.Persona.EstadoCivil:
                            datos_a_escribir["ESTADOCIVIL_D"] = empleado.Empleado.Persona.EstadoCivil.EstadoCivil
                        else:
                            datos_a_escribir["ESTADOCIVIL_D"] = ""
                        if empleado.Empleado.Persona.Nacionalidad:
                            datos_a_escribir["NACIONALIDAD_D"] = empleado.Empleado.Persona.Nacionalidad.Nacionalidad
                        else:
                            datos_a_escribir["NACIONALIDAD_D"] = ""
                        datos_a_escribir["SEXO_D"] = empleado.Empleado.Persona.Sexo
                        FechaNacimiento = empleado.Empleado.Persona.FechaNacimiento
                        FechaNacimiento = datetime.combine(FechaNacimiento, time())
                        FechaActual = datetime.today()
                        edad = relativedelta(FechaActual, FechaNacimiento).years
                        datos_a_escribir["EDAD_D"] = edad

                        if domicilio is not None:
                            datos_a_escribir["CALLE_D"] = str(domicilio.Vialidad) + str(domicilio.NumExterior)
                            datos_a_escribir["COLONIA_D"] = domicilio.idAsentamiento
                            datos_a_escribir["CP_D"] = str(domicilio.idCP)
                            Municipio = db.session.query(kMunicipio).filter(kMunicipio.idMunicipio == domicilio.idMunicipio).order_by(kMunicipio.Consecutivo.desc()).first()
                            datos_a_escribir["MUNICIPIO_D"] = Municipio.Municipio
                            Entidad = db.session.query(kEntidad).filter(kEntidad.idEntidad == domicilio.idEntidad).order_by(kEntidad.Consecutivo.desc()).first()
                            datos_a_escribir["ENTIDAD_D"] = Entidad.Entidad
                        else:
                            datos_a_escribir["CALLE_D"] = ""
                            datos_a_escribir["COLONIA_D"] = ""
                            datos_a_escribir["CP_D"] = ""
                            datos_a_escribir["MUNICIPIO_D"] = ""
                            datos_a_escribir["ENTIDAD_D"] = ""


                        datos_a_escribir["TELEFONO_D"] = empleado.Empleado.Persona.TelCasa

                        if TipoEmpleado == 1:
                            Puesto = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = empleado.idPuesto).first()
                            CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = empleado.idCentroCosto).first()
                            datos_a_escribir["CC_D"] = CentroCosto.CentroCosto
                            datos_a_escribir["CLAVEPRESUPUESTAL_D"] = ""
                            datos_a_escribir["NIVEL_D"] = Puesto.Nivel
                        else:
                            datos_a_escribir["CC_D"] = empleado.Puesto.CentroCostos.CentroCosto
                            datos_a_escribir["CLAVEPRESUPUESTAL_D"] = empleado.Puesto.CodigoPresupuestal
                            datos_a_escribir["NIVEL_D"] = empleado.Puesto.NivelSalarial

                        FechaInicio = datetime.combine(empleado.FechaInicio, datetime.min.time())
                        FechaInicio = FechaInicio.strftime("%d-%m-%Y")
                        datos_a_escribir["FECHAINICIO_D"] = FechaInicio

                        # for row in plantilla.iter_rows():
                        #     for cell in row:
                        #         if cell.value and isinstance(cell.value, str):
                        #             for key, value in datos_a_escribir.items():
                        #                 cell.value = cell.value.replace(f"%{key}%", str(value))

                        # for row in range(1, plantilla.used_range.last_cell.row + 1):
                        #     for col in range(1, plantilla.used_range.last_cell.column + 1):
                        #         cell = plantilla.cells(row, col)
                        #         if cell.value and isinstance(cell.value, str):
                        #             for key, value in datos_a_escribir.items():
                        #                 cell.value = cell.value.replace(f"%{key}%", str(value))

                        rango = plantilla.used_range
                        valores = rango.value

                        for i, fila in enumerate(valores):
                            for j, celda in enumerate(fila):
                                if celda in datos_a_escribir:
                                    plantilla[i, j + 1].value = datos_a_escribir[celda]

                        #nombre_archivo = "Nombramiento_" + str(empleado.Empleado.NumeroEmpleado)+ '_' + str(quincena) + ".xlsx"
                        
                        plantilla.api.ExportAsFixedFormat(0, ruta_pdf)
                        wb.save("rh/reportes/archivos/movimientos/" + nombre_archivo)
                        wb.close()
                        excel_app.quit()

                else:
                    print("El archivo existe")

                lista_archivos.append(nombre_archivo_pdf)

            else:
                respuesta = False

        print(lista_archivos)

    if movimiento == "2":
        #empleado_baja = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idTipoMovimiento == 3, rMovimientoEmpleado.idQuincena == quincena, rMovimientoEmpleado.idTipoEmpleado == TipoEmpleado, rMovimientoEmpleado.idPersonaMod == idPersona).first()
        lista_empleados = lista_empleados.filter(rMovimientoEmpleado.idTipoMovimiento == 3).all()

        for empleado_baja in lista_empleados:
            if empleado_baja:
                empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_baja.idPersonaMod).order_by(rEmpleadoPuesto.FechaInicio.desc()).first()

                nombre_archivo = "Baja_" + str(empleado.Empleado.NumeroEmpleado) + "_" + str(quincena) + ".xlsx"
                nombre_archivo_pdf = "Baja_" + str(empleado.Empleado.NumeroEmpleado) + "_" + str(quincena) + ".pdf"
                ruta_pdf = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos", nombre_archivo_pdf)

                if not os.path.isfile("rh/reportes/archivos/movimientos/" + nombre_archivo):

                    #ws = openpyxl.load_workbook(filename="rh/reportes/archivos/PLANTILLA FORMATO AVISO DE BAJA.xlsx")
                    #plantilla = ws.active

                    excel_app = xw.App(visible=False)
                    wb = xw.Book("rh/reportes/archivos/PLANTILLA FORMATO AVISO DE BAJA.xlsx")
                    plantilla = wb.sheets[0]

                    if empleado:
                        TipoEmpleado = empleado.Empleado.idTipoEmpleado
                        #hoja = wb.active

                        datos_a_escribir["FOLIO_D"] = empleado_baja.idMovimientoEmpleado
                        datos_a_escribir["APPATERNO_D"] = empleado.Empleado.Persona.ApPaterno
                        datos_a_escribir["APMATERNO_D"] = empleado.Empleado.Persona.ApMaterno
                        datos_a_escribir["NOMBRE_D"] = empleado.Empleado.Persona.Nombre
                        datos_a_escribir["RFC_D"] = empleado.Empleado.Persona.RFC
                        if TipoEmpleado == 1:
                            Puesto = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = empleado.idPuesto).first()
                            CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = empleado.idCentroCosto).first()
                            datos_a_escribir["CLAVEPRESUPUESTAL_D"] = ""
                            datos_a_escribir["NIVEL_D"] = Puesto.Nivel
                            datos_a_escribir["CC_D"] = CentroCosto.CentroCosto
                        else:
                            datos_a_escribir["CLAVEPRESUPUESTAL_D"] = empleado.Puesto.CodigoPresupuestal
                            datos_a_escribir["NIVEL_D"] = empleado.Puesto.NivelSalarial
                            datos_a_escribir["CC_D"] = empleado.Puesto.idCentroCosto

                        datos_a_escribir["CAUSABAJA_D"] = empleado.idCausaBaja
                        datos_a_escribir["NUMEMPLEADO_D"] = empleado.Empleado.NumeroEmpleado
                        datos_a_escribir["CURP_D"] = empleado.Empleado.Persona.CURP

                        FechaBaja = datetime.combine(empleado.FechaTermino, datetime.min.time())
                        FechaBaja = FechaBaja.strftime("%d-%m-%Y")
                        datos_a_escribir["FECHABAJA_D"] = FechaBaja

                        rango = plantilla.used_range
                        valores = rango.value

                        for i, fila in enumerate(valores):
                            for j, celda in enumerate(fila):
                                if celda in datos_a_escribir:
                                    plantilla[i, j].value = datos_a_escribir[celda]

                        # for row in plantilla.iter_rows():
                        #     for cell in row:
                        #         if cell.value and isinstance(cell.value, str):
                        #             for key, value in datos_a_escribir.items():
                        #                 cell.value = cell.value.replace(f"%{key}%", str(value))
                        
                        plantilla.api.ExportAsFixedFormat(0, ruta_pdf)
                        wb.save("rh/reportes/archivos/movimientos/" + nombre_archivo)
                        wb.close()
                        excel_app.quit()
                        respuesta= True

                else:
                    print("El archivo existe")
            
                lista_archivos.append(nombre_archivo_pdf)

            else:
                respuesta = False

    if movimiento == "3":
        todos = db.session.query(rMovimientoEmpleado).filter(rMovimientoEmpleado.idQuincena == quincena, rMovimientoEmpleado.idTipoEmpleado == TipoEmpleado).all()

        if TipoEmpleado == "1":
            nombre_archivo = "Movimientos_Honorarios_" + str(quincena) + ".xlsx"
            nombre_archivo_pdf = "Movimientos_Honorarios_" + str(quincena) + ".pdf"
        elif TipoEmpleado == "2":
            nombre_archivo = "Movimientos_Plaza_Federal_" + str(quincena) + ".xlsx"
            nombre_archivo_pdf = "Movimientos_Plaza_Federal_" + str(quincena) + ".pdf"

        ruta_pdf = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos", nombre_archivo_pdf)

        if not os.path.isfile("rh/reportes/archivos/movimientos/" + nombre_archivo):
            excel_app = xw.App(visible=False)

            cont = 1
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

            #ws = openpyxl.load_workbook(filename="rh/reportes/archivos/PLANTILLA REPORTE DE MOVIMIENTOS.xlsx")
            #plantilla = ws.active

            # Cargar una plantilla existente
            plantilla_wb = xw.Book("rh/reportes/archivos/PLANTILLA REPORTE DE MOVIMIENTOS.xlsx")
            plantilla = plantilla_wb.sheets[0]  
            for empleado_comb in todos:
                empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = empleado_comb.idPersonaMod).first()
                idTipoEmpleado = empleado.Empleado.idTipoEmpleado
                if empleado:
                    plantilla["A" + str(6 + cont)].value = cont
                    plantilla["B" + str(6 + cont)].value = str(datetime.now().year) +  str(quincena)
                    plantilla["C" + str(6 + cont)].value = empleado.Empleado.NumeroEmpleado
                    plantilla["D" + str(6 + cont)].value = empleado.Empleado.Persona.RFC
                    plantilla["E" + str(6 + cont)].value = empleado.Empleado.Persona.CURP
                    plantilla["F" + str(6 + cont)].value = empleado.Empleado.Persona.ApPaterno + " " + empleado.Empleado.Persona. ApMaterno + " " + empleado.Empleado.Persona.Nombre
                    plantilla["G" + str(6 + cont)].value = empleado_comb.idMovimientoEmpleado
                    if empleado_comb.idTipoMovimiento == 1 or empleado_comb.idTipoMovimiento == 2:
                        plantilla["H" + str(6 + cont)].value = "A"
                    elif empleado_comb.idTipoMovimiento == 3:
                        plantilla["H" + str(6 + cont)].value = "B"
                    if idTipoEmpleado == 2:
                        plantilla["I" + str(6 + cont)].value = ""
                        plantilla["J" + str(6 + cont)].value = ""
                        plantilla["K" + str(6 + cont)].value = empleado.Puesto.NivelSalarial
                        plantilla["L" + str(6 + cont)].value = ""
                        plantilla["M" + str(6 + cont)].value = ""
                        plantilla["N" + str(6 + cont)].value = empleado.Puesto.Puesto
                        plantilla["O" + str(6 + cont)].value = ""
                        plantilla["P" + str(6 + cont)].value = ""
                        plantilla["Q" + str(6 + cont)].value = empleado.Puesto.CentroCostos.CentroCosto
                    else:
                        Puesto = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = empleado.idPuesto).first()
                        CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = empleado.idCentroCosto).first   ()
                        plantilla["I" + str(6 + cont)].value = ""
                        plantilla["J" + str(6 + cont)].value = ""
                        plantilla["K" + str(6 + cont)].value = Puesto.Nivel
                        plantilla["L" + str(6 + cont)].value = ""
                        plantilla["M" + str(6 + cont)].value = ""
                        plantilla["N" + str(6 + cont)].value = Puesto.PuestoHonorarios
                        plantilla["O" + str(6 + cont)].value = ""
                        plantilla["P" + str(6 + cont)].value = ""
                        plantilla["Q" + str(6 + cont)].value = CentroCosto.CentroCosto
                    plantilla["R" + str(6 + cont)].value = ""
                    plantilla["S" + str(6 + cont)].value = ""
                    plantilla["T" + str(6 + cont)].value = empleado.Observaciones
                    cont = cont + 1

            plantilla.api.ExportAsFixedFormat(0, ruta_pdf)
            plantilla_wb.save("rh/reportes/archivos/movimientos/" + nombre_archivo)
            plantilla_wb.close()
            excel_app.quit()

            if len(todos) > 0:
                respuesta = True
            else:
                respuesta = False

        else:
            print("El archivo ya existe")

        lista_archivos.append(nombre_archivo_pdf)

    if len(lista_archivos) > 1:
        print("Es > 1")
        #zip_buffer = BytesIO()
        archivo_zip = "Nombramientos_" + str(quincena) + ".zip"
        with zipfile.ZipFile(os.path.join("rh/reportes/archivos/movimientos/", archivo_zip), 'w') as zip_file:
            for archivo in lista_archivos:
                if archivo.endswith('.pdf'):
                    ruta_archivo = os.path.join("rh/reportes/archivos/movimientos/", archivo)
                    print(ruta_archivo)
                    zip_file.write(ruta_archivo, arcname=archivo)

            zip_file.close()

        archivo_generado = archivo_zip

    elif len(lista_archivos) == 0:
        archivo_generado = ""

    else:
        print("Es < 1")
        archivo_generado = lista_archivos[0]

    return jsonify({"url_descarga": url_for("reportes.descargar_reporte", nombre_archivo=archivo_generado), "respuesta": respuesta})

@reportes.route("/rh/reportes/descargar-reporte/<nombre_archivo>")
def descargar_reporte(nombre_archivo):
    dir = os.path.join(current_app.root_path, "rh", "reportes", "archivos", "movimientos")
    return send_from_directory(directory=dir, path=nombre_archivo, as_attachment=True)