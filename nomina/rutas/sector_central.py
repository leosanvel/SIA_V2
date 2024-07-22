from .rutas import nomina
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_, func
from datetime import date, datetime
from catalogos.modelos.modelos import *
from nomina.modelos.modelos import *
from app import db

import os
import pandas as pd

@nomina.route('/nomina/sector-central', methods = ['POST', 'GET'])
def sector_central():
    anio_act = date.today().year
    AnioFiscal = db.session.query(kAnioFiscal).filter(kAnioFiscal.idAnioFiscal >= anio_act - 1).order_by(kAnioFiscal.idAnioFiscal).all()

    return render_template('/sector_central.html', title='Tabulador por ZE',
                           AnioFiscal = AnioFiscal,)

@nomina.route('/nomina/buscar-sector-central', methods = ['POST', 'GET'])
def buscar_sector_central():
    AnioFiscal = request.form.get("AnioFiscal")
    lista = []

    ZonasEconomicas = db.session.query(rZonaEconomica).filter_by(idAnioFiscal = AnioFiscal).all()         
    if ZonasEconomicas:
        for ZonaEconomica in ZonasEconomicas:
            lista.append({"idAnioFiscal":ZonaEconomica.idAnioFiscal,"idZonaEconomica":ZonaEconomica.idZonaEconomica,"idNivel":ZonaEconomica.idNivel,"SueldoBase":ZonaEconomica.SueldoBase,"CompensacionGarantizada":ZonaEconomica.CompensacionGarantizada})        
        respuesta = 0
    else:
        respuesta = 1

    return jsonify({"respuesta":respuesta,"lista":lista,})

@nomina.route('/nomina/extraer-archivoze', methods = ['POST'])
def extraer_concepto_archivo():
    archivo = request.files['archivo']
    if archivo and archivo.filename.endswith('.csv'):
        try:
            df = pd.read_csv(archivo)
        except UnicodeDecodeError:
            archivo.seek(0)
            df = pd.read_csv(archivo, encoding='latin1')
        resultados = []
        contador = 0
        try:
            for index, row in df.iterrows():
                if row['AÑO_FISCAL'] != "":
                    anio_fiscal = row['AÑO_FISCAL']
                    zona_economica = row['ZONA_ECONOMICA']
                    id_nivel = row['NIVEL']                
                    datos_archivo = {
                        "idAnioFiscal": anio_fiscal,
                        "idZonaEconomica": zona_economica,
                        "idNivel": id_nivel,
                        "SueldoBase": row['SUELDO_BASE'],
                        "CompensacionGarantizada": row['COMPENSACION_GARANTIZADA'],
                    }
                    tabze = db.session.query(rZonaEconomica).filter_by(idAnioFiscal = anio_fiscal, idZonaEconomica = zona_economica, idNivel = id_nivel).first()
                    if tabze:
                        tabze.update(**datos_archivo)
                    else:    
                        nuevo_registro = rZonaEconomica(**datos_archivo)
                        db.session.add(nuevo_registro)
                    db.session.commit()

                    resultados.append(datos_archivo)
                    contador = contador + 1
                else:
                    print("Termina recorrido o archivo vacío")
            if contador >= 1:
                print("guardado")
                return jsonify({"Resultado": 1, "Informacion": "guardado"})
            else:
                print("Revisar formato del archivo")
                return jsonify({"Resultado": 4, "Informacion": "El archivo no contiene el formato adecuado y/o se encuentra vacío."})
        
        except Exception as er:
            print(er)
            return jsonify({"Resultado": 3, "Informacion": "La extracción de información falló."})        
    else:
        return jsonify({"Resultado": 2, "Informacion": "No se recibió un archivo CSV."})


@nomina.route('/nomina/guardar-tabulador', methods = ['POST'])
def guardar_tabulador():
    anio_fiscal = request.form.get("idAnioFiscal")
    zona_economica = request.form.get("idZonaEconomica")
    nivel =  request.form.get("idNivel")
    sueldo_base = request.form.get("SueldoBase")
    compensacion_garantizada = request.form.get("CompensacionGarantizada")
    datos = {
        "idAnioFiscal": anio_fiscal,
        "idZonaEconomica": zona_economica,
        "idNivel": nivel,
        "SueldoBase": sueldo_base,
        "CompensacionGarantizada": compensacion_garantizada,
    }
    tabze = db.session.query(rZonaEconomica).filter_by(idAnioFiscal = anio_fiscal , idZonaEconomica = zona_economica , idNivel = nivel ).first()
    if tabze:
        tabze.update(**datos)
        db.session.commit()
        respuesta = 0
    else:
        respuesta = 1
    return jsonify({"respuesta": respuesta})