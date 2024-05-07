from flask import render_template, request, jsonify, url_for, current_app
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from datetime import time, date, datetime
import locale
import openpyxl
from openpyxl.styles import NamedStyle, Border, Side, Alignment
from sqlalchemy import and_, or_
from collections import defaultdict
from .gestion_asistencias import gestion_asistencias

from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import kQuincena, kTipoEmpleado
from nomina.modelos.modelos import rNominaPersona

import os
from flask import send_from_directory

# Establecer la configuración regional a español (para la fecha)
locale.setlocale(locale.LC_TIME, 'es_ES')

@gestion_asistencias.route('/rh/gestion-asistencias/reporte-incidencias', methods = ['POST', 'GET'])
def enviar_nomina():
    Quincenas = db.session.query(kQuincena).order_by(kQuincena.idQuincena).all()
    Tipos_Empleados = db.session.query(kTipoEmpleado).order_by(kTipoEmpleado.TipoEmpleado).all()

    return render_template('/reporte_incidencias.html', title='Envío a Nómina',
                           Quincenas = Quincenas,
                           Tipos_Empleados = Tipos_Empleados)

@gestion_asistencias.route('/rh/gestion-asistencias/vista-previa', methods = ['POST'])
def vista_previa():
    mapeo_nombres = {
        'NumQuincena': 'NumeroQuincena',
        'TipoEmpleado': 'TipoEmpleado',
    }
    nomina_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    lista_nomina = procesar_nomina(nomina_data,True)
    
    # if "NoChecador" in lista_nomina or "NoIncidencias" in lista_nomina:

    # if "NoChecador" in lista_nomina:
    #     return jsonify({"NoChecador": True})
    # elif "NoIncidencias" in lista_nomina:
    #     return jsonify({"NoIncidencias": True})
    return jsonify(lista_nomina)

@gestion_asistencias.route('/rh/gestion-asistencias/generar-reporte-incidencias', methods = ['POST', 'GET'])
def genera_reporte_incidencias():

    mapeo_nombres = {
        'NumQuincena': 'NumeroQuincena',
        'TipoEmpleado': 'TipoEmpleado',
    }
    nomina_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    
    lista_nomina = procesar_nomina(nomina_data)
    if(lista_nomina["NoChecador"] or lista_nomina["NoIncidencias"]):
        return jsonify(lista_nomina)
    fecha_actual = datetime.now()
    quincena = db.session.query(kQuincena).filter(kQuincena.idQuincena == nomina_data["NumeroQuincena"]).one()
    dias_quincena = quincena.FechaFin - quincena.FechaInicio
    dias_quincena = dias_quincena.days
    
    #GENERAR TNOMINA
    nomina_actual={
        "idQuincena": quincena.idQuincena,
        "Descripcion": quincena.Descripcion + ' DE ' + str(quincena.FechaFin.year),
        "Estatus": 1,
        "idPersonaEmisor": current_user.id,
        "PeriodoQuincena": quincena.FechaFin.year,
    }

    try:
        nomina_existente = db.session.query(tNomina).filter_by(idQuincena = nomina_actual['idQuincena'], PeriodoQuincena = nomina_actual['PeriodoQuincena']).one()
        # Si llegamos aquí, significa que ya existe la nómina
        archivo_generado = "Reporte_incidencia_" + nomina_data["NumeroQuincena"] + "_tipo_" + nomina_data["TipoEmpleado"] + "_" + str(quincena.FechaFin.year) + ".xlsx"

        return jsonify({"url_descarga": url_for('gestion_asistencias.descargar_archivo', nombre_archivo = archivo_generado), "respuesta":"existente"})

        # return jsonify({"respuesta":"existente"})
    except NoResultFound:
        nueva_nomina = tNomina(**nomina_actual)
        db.session.add(nueva_nomina)
        db.session.commit()
    numeros_empleados = db.session.query(rEmpleado.idPersona).filter_by(idTipoEmpleado = nomina_data["TipoEmpleado"],Activo = 1).all()
            # Extrae los números de empleado de la lista de tuplas
    numeros_empleados = [numero[0] for numero in numeros_empleados]

    lista_nomina_aux = lista_nomina["lista_nomina"]
    # Crear un diccionario que mapee los empleados por su ID
    empleados_con_incidencias = {str(empleado["idPersona"]): empleado for empleado in lista_nomina_aux}

    for id_empleado in numeros_empleados:
        empleado = empleados_con_incidencias.get(str(id_empleado))
        if empleado:
            # Calcular los días laborados
            diasLaborados = dias_quincena - empleado["NumeroDias"]
        else:
            # Si el empleado no está en la lista, asignar todos los días de la quincena
            diasLaborados = dias_quincena

        #GENERAR TNOMINA2
        nomina_persona={
            "idNomina" : nueva_nomina.idNomina,
            "idPersona" : id_empleado,
            "DiasLaborados": diasLaborados,
        }

        nueva_nomina_persona = rNominaPersona(**nomina_persona)
        db.session.add(nueva_nomina_persona)
        db.session.commit()




    # GENERAR DOCUMENTO
    # Cargar la plantilla de Excel
    wb = openpyxl.load_workbook(filename="rh/gestion_asistencias/archivos/Plantilla_Reporte_Incidencias.xlsx", rich_text=True)
    hoja = wb.active

    # Estilos para las celdas
    # Estilo con bordes
    estilo_con_bordes = NamedStyle(name="con_bordes")
    estilo_con_bordes.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    # Estilo con texto centrado y bordes
    estilo_texto_centrado = NamedStyle(name="texto_centrado")
    estilo_texto_centrado.alignment = Alignment(horizontal='center', vertical='center')
    estilo_texto_centrado.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    
    #Información
    datos_a_insertar = {
        'AÑO': str(quincena.FechaFin.year),
        'FECHA': fecha_actual.strftime("%d de %B de %Y"),
        'QUINCENA': str(quincena.Descripcion) + ' DE ' + str(quincena.FechaFin.year)
    }

    # Llenar las celdas de marcadores de posición con datos
    for row in hoja.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                for key, value in datos_a_insertar.items():
                    cell.value = cell.value.replace(f"%{key}%", str(value))

    fila_actual = 11

    for empleado in lista_nomina_aux:
        
        # Insertar una nueva fila en blanco
        hoja.insert_rows(fila_actual)

        rango_celdas = hoja['B'+ str(fila_actual) + ':I'+ str(fila_actual)]
        
        # Aplicar el estilo con bordes a cada celda en el rango
        for fila in rango_celdas:
            for celda in fila:
                celda.style = estilo_con_bordes

        # Llenar información
        hoja['B'+str(fila_actual)] = empleado["N"]
        hoja['B'+str(fila_actual)].style = estilo_texto_centrado
        hoja['C'+str(fila_actual)] = empleado["ADSCRIP"]
        hoja['C'+str(fila_actual)].style = estilo_texto_centrado
        hoja['D'+str(fila_actual)] = empleado["Nivel"]
        hoja['D'+str(fila_actual)].style = estilo_texto_centrado
        hoja['E'+str(fila_actual)] = empleado["NombrePersona"]
        hoja['F'+str(fila_actual)] = empleado["RFC"]
        hoja['G'+str(fila_actual)] = empleado["NumeroEmpleado"]
        hoja['G'+str(fila_actual)].style = estilo_texto_centrado
        hoja['H'+str(fila_actual)] = empleado["NumeroDias"]
        hoja['H'+str(fila_actual)].style = estilo_texto_centrado
        hoja['I'+str(fila_actual)] = empleado["DiasIncidencias"]
        hoja['I'+str(fila_actual)].style = estilo_texto_centrado
        fila_actual += 1
    # Guardar el archivo Excel con datos llenos
    wb.save("rh/gestion_asistencias/archivos/generados/Reporte_incidencia_" + nomina_data["NumeroQuincena"] + "_tipo_" + nomina_data["TipoEmpleado"] + "_" + datos_a_insertar['AÑO'] + ".xlsx")


    archivo_generado = "Reporte_incidencia_" + nomina_data["NumeroQuincena"] + "_tipo_" + nomina_data["TipoEmpleado"] + "_" + datos_a_insertar['AÑO'] + ".xlsx"

    return jsonify({"url_descarga": url_for('gestion_asistencias.descargar_archivo', nombre_archivo=archivo_generado), "respuesta":"creado"})


# -------------------------------------------------------------
@gestion_asistencias.route('/descargar_archivo/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "rh", "gestion_asistencias", "archivos", "generados")
    return send_from_directory(directory=directorio_archivos, path=nombre_archivo, as_attachment=True)

