from .rutas import prestaciones
from flask import render_template, request, jsonify, current_app
from flask_login import current_user
import os
from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto, rEmpleadoSueldo
from rh.gestion_empleados.modelos.empleado import rEmpleado
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from datetime import datetime

@prestaciones.route('/prestaciones/importar-conceptos')
def importar_conceptos():
    conceptos = db.session.query(kConcepto).filter_by(ExtraeArchivo = 1).all()
    print(conceptos)
    return render_template('/importar_conceptos.html', title ='Importar conceptos',
                            current_user=current_user,
                            conceptos = conceptos)


@prestaciones.route('/prestaciones/filtrar-conceptos-extrae-archivo', methods = ['POST'])
def filtrar_conceptos_extraeArchivo():
    conceptos = db.session.query(kConcepto).filter_by(ExtraeArchivo = 1).all()
    lista_conceptos = []
    for elemento in conceptos:
        if elemento is not None:
            elemento_dict = elemento.__dict__
            elemento_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_conceptos.append(elemento_dict)
    if not lista_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_conceptos)

@prestaciones.route('/prestaciones/extraer-concepto-de-archivo', methods = ['POST'])
def extraer_concepto_archivo():
    archivo = request.files['archivo']
    idTipoConcepto = request.form.get('idTipoConcepto')
    idConcepto = request.form.get('idConcepto')
    
# Verificar que se haya recibido un archivo y que sea un archivo de texto
    if archivo and archivo.filename.endswith('.txt'):

        # Leer el contenido del archivo
        contenido = archivo.read().decode('utf-8')

        concepto = porcentaje = monto = None
        lista_empleados = []
        # Buscar las variables en el archivo
        for linea in contenido.split('\n'):
            if linea:
                empleado = {}
                empleado["Ramo"] = linea[0:3].strip()
                empleado["PAGSUBPAG"] = linea[3:8].strip()
                empleado["NumeroISSSTE"] = linea[8:18].strip()
                empleado["RFC"] = linea[18:31].strip()
                empleado["Nombre"] = linea[31:71].strip()
                empleado["ClaveCobro"] = linea[71:101].strip()
                empleado["TPOD"] = linea[101:102].strip()
                empleado["PzoQna"] = linea[102:105].strip()
                empleado["Periodo1"] = linea[105:111].strip()
                empleado["Periodo2"] = linea[111:117].strip()
                empleado["Concepto"] = linea[117:119].strip()
                empleado["NumeroPrestamo"] = linea[167:177].strip()
                
                importe_str = linea[119:126].strip()
                if importe_str:  # Verifica si la cadena no está vacía
                    empleado["Importe"] = round(float(importe_str)/100, 2)
                else:
                    empleado["Importe"] = "0.0"

                # Añade el empleado a la lista
                lista_empleados.append(empleado)
        # Verificar si se encuentra el directorio
        # directorio_archivos = os.path.join(current_app.root_path, "prestaciones", "docs")
        # if not os.path.exists(directorio_archivos):
        #     os.makedirs(directorio_archivos)
        # nombre_unico = obtener_nombre_unico("Archivo.txt")
        # filepath = os.path.join(directorio_archivos, nombre_unico)
        # archivo.save(filepath)
        


        if lista_empleados:
            return jsonify({"Obtenido": True, "lista_empleados": lista_empleados})
        else:
            return jsonify({"ErrorLectura": True, "mensaje": "La extracción de información falló."})
    else:
        return jsonify({"ArchivoInvalido": True, "mensaje": "No se recibió un archivo de texto o el archivo está vacío"})
   
def obtener_nombre_unico(nombre_original):
    base, extension = os.path.splitext(nombre_original)
    contador = 1
    nombre_unico = f"{base}_{contador}{extension}"
    directorio_archivos = os.path.join(current_app.root_path, "prestaciones", "docs")
    ruta_completa = os.path.join(directorio_archivos, nombre_unico)
    
    while os.path.exists(ruta_completa):
        contador += 1
        nombre_unico = f"{base}_{contador}{extension}"
        ruta_completa = os.path.join(directorio_archivos, nombre_unico)
    
    return nombre_unico