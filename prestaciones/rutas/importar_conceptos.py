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

import pandas as pd

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
    if archivo and archivo.filename.endswith('.csv'):
        try:
            # Intentar leer el archivo con la codificación predeterminada utf-8
            try:
                df = pd.read_csv(archivo)
            except UnicodeDecodeError:
                # Si falla, intentar leer el archivo con la codificación latin1
                archivo.seek(0)  # Volver al inicio del archivo
                df = pd.read_csv(archivo, encoding='latin1')
            
            # Crear una nueva tabla con RFC único y suma de RETENCION_MENSUAL
            resumen_df = df.groupby('RFC')['RETENCION_MENSUAL'].sum().reset_index()
            
            # Imprimir el resultado
            print(resumen_df)
            
            lista_empleados = []
            return jsonify({"Obtenido": True, "lista_empleados": lista_empleados})
        
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return jsonify({"ErrorLectura": True, "mensaje": "La extracción de información falló."})
    else:
        return jsonify({"ArchivoInvalido": True, "mensaje": "No se recibió un archivo CSV"})


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