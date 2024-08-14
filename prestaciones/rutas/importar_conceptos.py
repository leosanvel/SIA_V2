from .rutas import prestaciones
from flask import render_template, request, jsonify, current_app
from flask_login import current_user
import os
from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto, rEmpleadoSueldo
from rh.gestion_empleados.modelos.empleado import rEmpleado, tPersona
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import asc
from datetime import datetime

import pandas as pd

@prestaciones.route('/prestaciones/importar-conceptos')
def importar_conceptos():
    conceptos = db.session.query(kConcepto).filter_by(ExtraeArchivo = 1).all()
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
    idTipoConcepto = request.form.get('idTipoConcepto', None)
    idConcepto = request.form.get('idConcepto', None)
    
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


            # ELIMINAR CONCEPTOS ANTERIORES
            elimina = db.session.query(rEmpleadoConcepto).filter_by(idTipoConcepto=idTipoConcepto, idConcepto=idConcepto).delete()
            print("Conceptos eliminados: " + str(elimina))
            
            # Crear una lista para almacenar los resultados
            resultados = []

            # Iterar sobre cada fila del DataFrame original
            for index, row in df.iterrows():
                RFC = row['RFC']
                try:
                    # Realizar la consulta para obtener la persona correspondiente al RFC
                    try:
                        persona = db.session.query(tPersona).filter_by(RFC=RFC).one()
                    except NoResultFound:
                        # Buscar utilizando el número de empleado si no se encuentra por RFC
                        NumEmpleado = row['CLAVE_EMPLEADO']
                        empleado = db.session.query(rEmpleado).filter_by(NumeroEmpleado=NumEmpleado).one()
                        persona = db.session.query(tPersona).filter_by(idPersona=empleado.idPersona).one()

                    
                    # Crear el diccionario con los datos necesarios
                    NumeroContrato = row['No_CREDITO']
                    idPersona = persona.idPersona

                    concepto_data = {
                        "idPersona": idPersona,
                        "idTipoConcepto": idTipoConcepto,
                        "idConcepto": idConcepto,
                        "NumeroContrato": NumeroContrato,
                        "Porcentaje": 0,
                        "Monto": row['RETENCION_MENSUAL'] / 2,
                        "FechaInicio": None,
                        "FechaFin": None,
                        "PagoUnico": 0,
                    }
                    nuevo_concepto = None
                    try:
                        concepto_a_modificar = db.session.query(rEmpleadoConcepto).filter_by(
                            idPersona=idPersona, idTipoConcepto=idTipoConcepto, idConcepto=idConcepto, NumeroContrato=NumeroContrato
                        ).one()
                        concepto_data['FechaModificacion'] = datetime.now()
                        concepto_a_modificar.update(**concepto_data)
                        
                    except NoResultFound:
                        concepto_data['FechaModificacion'] = datetime.now() 
                        concepto_data['FechaAlta'] = datetime.now()
                        nuevo_concepto = rEmpleadoConcepto(**concepto_data)
                        db.session.add(nuevo_concepto)

                    # Realizar cambios en la base de datos
                    db.session.commit()
       
                    concepto_data["Nombre"] = persona.Nombre
                    concepto_data["Apellidos"] = persona.ApPaterno + " " + persona.ApMaterno
                    concepto_data["RFC"] = persona.RFC
                    # Añadir el diccionario a la lista de resultados
                    resultados.append(concepto_data)
                    
                except NoResultFound:
                    # Manejar el caso donde no se encuentra la persona con el RFC dado
                    print(f"No se encontró la persona con el RFC: {RFC}")
                    # Añadir el diccionario de error a la lista de resultados
                    resultados.append({"errorRFC": RFC})
                except MultipleResultsFound:
                    # Manejar el caso donde se encuentran múltiples personas con el RFC dado
                    print(f"Se encontraron múltiples personas con el RFC: {RFC}")
                    # Añadir el diccionario de error a la lista de resultados
                    resultados.append({"errorRFC": RFC, "mensaje": "Se encontraron múltiples personas con el RFC"})
                except Exception as e:
                    # Manejar otros posibles errores
                    print(f"Error procesando la fila {index}: {e}")
                    # Añadir el diccionario de error a la lista de resultados
                    resultados.append({"errorRFC": RFC, "mensaje": str(e)})

            return jsonify({"Obtenido": True, "resultados": resultados})
        
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