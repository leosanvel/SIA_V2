from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_, func
from datetime import datetime
from app import db

import openpyxl

@prestaciones.route('/prestaciones/cedula-fonacot', methods = ['POST', 'GET'])
def cedula_fonacot():
    return render_template('/cedula_fonacot.html', title='Cedula FONACOT',
                           )

@prestaciones.route('/prestaciones/cedula-fonacot', methods = ['POST', 'GET'])
def generar_cedula_fonacot():
    respuesta = 0
    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.title = "Cedula Fonacot"
    hoja.append(('Número empleado','Empleado','CURP','RFC', 'PUESTO', 'JEFE INMEDIATO'))
    #for empleado_nomina in empleados_nomina: 
    #    hoja.append(empleado_nomina)
    wb.save("nomina/Doctos/Reporte_General.xlsx")
    respuesta = 1
    print("Proceso terminado")

    #return jsonify({"respuesta":respuesta,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo=nombre_archivo+'.',extencion_archivo='xlsx'),})