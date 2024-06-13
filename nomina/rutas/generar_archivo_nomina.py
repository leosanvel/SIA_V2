from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from autenticacion.modelos.modelos import *
from nomina.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import tPersona, rEmpleado

import openpyxl

@nomina.route('/nomina/generar-archivo-nomina', methods = ['POST', 'GET'])

def ArchivoNomina():
    Nominas = db.session.query(tNomina).filter_by(Estatus=2).all()
    return render_template('/archivo_nomina.html', title='Generar Archivo de Nómina',
                           Nominas=Nominas,
                           )

@nomina.route('/Nomina/ArchivoNomina', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_Archivo_Nomina():
    respuesta = 0
    numero_nomina = request.form.get("idNomina")
    nombre_archivo = ""
    Nomina = db.session.query(tNomina).filter_by(idNomina=numero_nomina,Estatus=2).first()
    if Nomina:
        nombre_archivo = Nomina.Nomina
        numero_quincena = Nomina.Quincena
        mes_pago = Nomina.FechaPago.strftime("%m")
        anio_pago = Nomina.FechaPago.strftime("%Y")
        nombre_carpeta = numero_quincena + mes_pago + anio_pago 
    
        empleados_nomina = []
        
        Empleados = db.session.query(rNominaPersonas.idCentroCosto.label("CentroCosto"),rNominaPersonas.idNivel.label("Nivel"),rNominaPersonas.idConcepto.label("Concepto"),rNominaPersonas.Importe.label("Importe"),tPersona.RFC.label("RFC")).filter_by(idNomina=numero_nomina).filter_by(idPersona = tPersona.idPersona).order_by(tPersona.RFC,rNominaPersonas.idConcepto).all()
        for Empleado in Empleados:            
            empleados_nomina = empleados_nomina + [(Empleado.CentroCosto,Empleado.Nivel,Empleado.RFC,Empleado.Concepto,Empleado.Importe)]

        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.title = Nomina.Nomina
        hoja.append(('N_ADSCRIP','N_NIVEL','N_RFC', 'N_CONCEPTO', 'N_IMPORTE'))
        for empleado_nomina in empleados_nomina: 
            hoja.append(empleado_nomina)
        wb.save("nomina/Doctos/"+nombre_carpeta+"/"+nombre_archivo+".xlsx")
        respuesta = 1
        print("Proceso terminado")
    else:
        print("Sin registros")

    return jsonify({"respuesta":respuesta,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo=nombre_archivo+'.',extencion_archivo='xlsx'),})