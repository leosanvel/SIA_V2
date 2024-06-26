from .puestos import puestos
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_, func
from datetime import datetime

from app import db
from rh.gestion_empleados.modelos.empleado import tPuesto
from catalogos.modelos.modelos import kRamo, kUA, kZonaEconomica, kTipoPlazaPuesto, kCaracterOcupacional, kTipoFuncion, kGrupo, kGrado, kNivel, kEstatusPuesto, kVigencia, kCentroTrabajo, kCentroCostos

import openpyxl

@puestos.route('/innovacion-normas/puestos/reporte-antecedente', methods = ['POST', 'GET'])
def reporte_antecedente():
    return render_template('/reporte_antecedente.html', title='Reporte de antecedente',
                           )

@puestos.route('/innovacion-normas/puestos/reporte-antecedente', methods = ['POST', 'GET'])
def generar_reporte_antecedente():
    respuesta = 0
    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.title = "Reporte General"
    hoja.append(('Número empleado','Empleado','CURP','RFC', 'PUESTO', 'JEFE INMEDIATO'))
    #for empleado_nomina in empleados_nomina: 
    #    hoja.append(empleado_nomina)
    wb.save("nomina/Doctos/Reporte_General.xlsx")
    respuesta = 1
    print("Proceso terminado")

    #return jsonify({"respuesta":respuesta,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo=nombre_archivo+'.',extencion_archivo='xlsx'),})