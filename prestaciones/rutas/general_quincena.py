from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import prestaciones
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import tPersona, rEmpleado, rEmpleadoPuesto
from dateutil.relativedelta import relativedelta
import openpyxl
import os

@prestaciones.route("/prestaciones/reporte-general-quincena", methods = ['POST', 'GET'])
def general_quincena():
    Quincenas = db.session.query(kQuincena).all()
    return render_template("/general_quincena.html", title = "General por quincena",
                           Quincenas = Quincenas)

@prestaciones.route('/prestaciones/genera-reporte-general-quincena', methods = ['POST', 'GET'])
def reporte_general_quincena():
    respuesta = 0
    numero_quincena = request.form.get("Quincenas")
    nombre_archivo = ""

    Quincena = db.session.query(kQuincena).filter_by(idQuincena=1).first()
    if Quincena:
        nombre_archivo = "GeneralxQuincena"
        nombre_carpeta = "Reporte"
    
        empleados_concepto = []
        strConcepto = ""
        total_registros = 0
        total_importe = 0
        total_descuento = 0
        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.title = "GeneralxQuincena"

        #conceptoempleado = db.session.query(rEmpleadoConcepto).filter(rEmpleadoConcepto.idConcepto.in_([3,50,51,55,57,64,65,94,100]),rEmpleadoConcepto.FechaFin>=Quincena.FechaInicio).order_by(rEmpleadoConcepto.idConcepto).all()
        conceptoempleado = db.session.query(rEmpleadoConcepto).filter(rEmpleadoConcepto.idConcepto.in_([3,50,51,55,57,64,65,94,100]),rEmpleadoConcepto.FechaModificacion>=Quincena.FechaInicio).order_by(rEmpleadoConcepto.idConcepto).all()
        
        for concepto in conceptoempleado:
            empleados = db.session.query(rEmpleado.NumeroEmpleado.label("NumeroEmpleado"),tPersona.RFC.label("RFC"),tPersona.Nombre.label("Nombre"),tPersona.ApPaterno.label("ApPaterno"),tPersona.ApMaterno.label("ApMaterno"),rEmpleadoPuesto.idNivel.label("Nivel"),rEmpleadoPuesto.idEstatusEP.label("EstatusPuesto")).filter_by(idPersona=concepto.idPersona,idTipoEmpleado=2,Activo=1).filter_by(idPersona = tPersona.idPersona).filter_by(idPersona = rEmpleadoPuesto.idPersona).first()
            if empleados:
                if empleados.EstatusPuesto == 1:
                   
                    fecha_inicio = concepto.FechaInicio  
                    fecha_fin = concepto.FechaFin      
                    meses = contar_meses_entre_fechas(fecha_inicio, fecha_fin)
                    plazo_quincenal = meses * 2

                    
                    if concepto.Porcentaje > 0:
                        descuento_quincenal = str(concepto.Porcentaje) + " %"
                        importe_descontar = 0.00
                    else:
                        descuento_quincenal = concepto.Monto
                        importe_descontar = plazo_quincenal * descuento_quincenal


                    
                    nombre_empleado = empleados.Nombre + ' ' + empleados.ApPaterno + ' ' + empleados.ApMaterno
                    #empleados_concepto = empleados_concepto + [(empleados.RFC,nombre_empleado,'',empleados.Nivel,concepto.FechaInicio,concepto.FechaFin,plazo_quincenal,importe_descontar,descuento_quincenal,concepto.idConcepto)]
                    
                    if strConcepto != concepto.idConcepto:                        
                        if len(strConcepto) > 0:
                           hoja.append(('','','','','','Total :',total_registros,total_importe,total_descuento))
                        hoja.append(('',''))
                        total_registros = 0
                        total_importe = 0
                        total_descuento = 0
                        hoja.append(('DIRECCION GENERAL DE ADMINISTRACION Y FINANZAS',''))
                        hoja.append(('DIRECCION DE RECURSOS HUMANOS',''))
                        hoja.append(('SUBDIRECCION DE PRESTACIONES',''))
                        nombreconcepto = db.session.query(kConcepto).filter_by(idTipoConcepto = concepto.idTipoConcepto, idConcepto = concepto.idConcepto, idTipoEmpleado = 2).first()
                        if nombreconcepto:
                            nombre_concepto = nombreconcepto.Concepto + " (" + concepto.idConcepto + "-" + concepto.idTipoConcepto + ")" 
                            hoja.append((nombre_concepto,''))
                        
                        hoja.append(('RFC','Nombre','Centro_Costo','Nivel','Fecha_Inicio','Fecha_Fin','Plazo Qnal','Importe a descontar','Descuento Quincenal'))                  
                    
                    total_registros = total_registros + 1
                    
                    if concepto.Porcentaje == 0:
                        total_importe = total_importe + importe_descontar
                        total_descuento = total_descuento + descuento_quincenal
                        print("")

                    hoja.append((empleados.RFC,nombre_empleado,'',empleados.Nivel,concepto.FechaInicio,concepto.FechaFin,plazo_quincenal,importe_descontar,descuento_quincenal))
                    strConcepto = concepto.idConcepto
        if total_registros > 0:
            hoja.append(('','','','','','Total :',total_registros,total_importe,total_descuento))

        wb.save("prestaciones/Doctos/"+nombre_carpeta+"/"+nombre_archivo+".xlsx")
        respuesta = 1
        print("Proceso terminado")
    else:
        print("Sin registros")

    

    return jsonify({"respuesta":respuesta,"url_descarga": url_for('prestaciones.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo=nombre_archivo+'.',extencion_archivo='xlsx'),})

@prestaciones.route('/prestaciones/Doctos/<nombrecarpeta>/<nombre_archivo><extencion_archivo>')
def descargar_archivo(nombrecarpeta,nombre_archivo,extencion_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "prestaciones", "Doctos", nombrecarpeta)
    return send_from_directory(directory=directorio_archivos, path=nombre_archivo+extencion_archivo, as_attachment=True)

def contar_meses_entre_fechas(fecha_inicio, fecha_fin):
    # Asegurarse de que fecha_inicio sea anterior a fecha_fin
    if fecha_inicio > fecha_fin:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
    
    # Calcular la diferencia en meses
    diferencia = relativedelta(fecha_fin, fecha_inicio)
    meses_totales = diferencia.years * 12 + diferencia.months 
    return meses_totales + 1