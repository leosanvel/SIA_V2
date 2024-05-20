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

    return render_template('/importar_conceptos.html', title ='Importar conceptos',
                            current_user=current_user)


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

    # Verificar que se haya recibido un archivo y que sea un archivo de texto
    if archivo and archivo.filename.endswith('.txt'):

        # Leer el contenido del archivo
        contenido = archivo.read().decode('utf-8')

        concepto = porcentaje = monto = None

        # Buscar las variables en el archivo
        for linea in contenido.split('\n'):
            if 'concepto' in linea:
                concepto = linea.split('=')[1].strip()
            elif 'porcentaje' in linea:
                porcentaje = linea.split('=')[1].strip()
            elif 'monto' in linea:
                monto = linea.split('=')[1].strip()

        # Verificar si se encontraron todas las variables
        print( "AQUI EMPIEZA")
        print(concepto)
        print(porcentaje)        
        print(monto)

        directorio_archivos = os.path.join(current_app.root_path, "prestaciones", "docs")
        if not os.path.exists(directorio_archivos):
            os.makedirs(directorio_archivos)
        nombre_unico = obtener_nombre_unico("Archivo.txt")
        filepath = os.path.join(directorio_archivos, nombre_unico)
        archivo.save(filepath)
        
        if concepto is not None or porcentaje is not None or monto is not None:
            return jsonify({"Obtenido": True, "concepto": concepto, "porcentaje": porcentaje, "monto": monto})
        else:
            return jsonify({"ErrorLectura": True, "mensaje": "No se encontraron todas las variables"})
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