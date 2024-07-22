from .rutas import nomina
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_, func
from datetime import date, datetime
from catalogos.modelos.modelos import *
from nomina.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import *
from prestaciones.modelos.modelos import *
from app import db

import os
import pandas as pd

@nomina.route('/nomina/mando-enlace', methods = ['POST', 'GET'])
def mando_enlace():
    anio_act = date.today().year
    AnioFiscal = db.session.query(kAnioFiscal).filter(kAnioFiscal.idAnioFiscal >= anio_act - 1).order_by(kAnioFiscal.idAnioFiscal).all()

    return render_template('/mando_enlace.html', title='Tabulador por ME',
                           AnioFiscal = AnioFiscal,)

@nomina.route('/nomina/buscar-mando-enlace', methods = ['POST', 'GET'])
def buscar_mando_enlace():
    AnioFiscal = request.form.get("AnioFiscal")
    lista = []

    MandosEnlaces = db.session.query(rTabuladorSalarial).filter_by(idAnioFiscal = AnioFiscal).order_by(rTabuladorSalarial.idGrupo,rTabuladorSalarial.idGrado,rTabuladorSalarial.idNivel).all()         
    if MandosEnlaces:
        for MandoEnlace in MandosEnlaces:
            lista.append({"idAnioFiscal":MandoEnlace.idAnioFiscal,"idGrupo":MandoEnlace.idGrupo,"idGrado":MandoEnlace.idGrado,"idNivel":MandoEnlace.idNivel,"PuntoInicial":MandoEnlace.PuntoInicial,"PuntoFinal":MandoEnlace.PuntoFinal,"SueldoBase":MandoEnlace.SueldoBase,"CompensacionGarantizada":MandoEnlace.CompensacionGarantizada})        
        respuesta = 0
    else:
        respuesta = 1

    return jsonify({"respuesta":respuesta,"lista":lista,})

@nomina.route('/nomina/extraer-archivome', methods = ['POST'])
def extraer_mando_enlace():
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
                if row['ID_GRUPO'] != "":
                    anio_fiscal = row['AÑO_FISCAL']
                    id_grupo = row["ID_GRUPO"]
                    id_grado = row["ID_GRADO"]
                    id_nivel = row['ID_NIVEL']

                    datos_archivo = {
                        "idAnioFiscal": anio_fiscal,
                        "idGrupo": id_grupo,
                        "idGrado": id_grado,
                        "idNivel": id_nivel,
                        "PuntoInicial": row['PUNTO_INICIAL'],
                        "PuntoFinal": row['PUNTO_FINAL'],
                        "SueldoBase": row['SUELDO_BASE'],
                        "CompensacionGarantizada": row['COMPENSACION_GARANTIZADA'],
                    }
                    tabme = db.session.query(rTabuladorSalarial).filter_by(idAnioFiscal = anio_fiscal, idGrupo = id_grupo, idGrado = id_grado, idNivel = id_nivel).first()
                    if tabme:
                        tabme.update(**datos_archivo)
                    else:    
                        nuevo_registro = rTabuladorSalarial(**datos_archivo)
                        db.session.add(nuevo_registro)
                    db.session.commit()
                    resultados.append(datos_archivo)
                    actualizar_sueldos_puestos(anio_fiscal,id_grupo,id_grado,id_nivel)
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

@nomina.route('/nomina/guardar-tabulador-mando-enlace', methods = ['POST'])
def guardar_tabulador_mando_enlace():
    anio_fiscal = request.form.get("idAnioFiscal")
    id_grupo = request.form.get("idGrupo")
    id_grado = request.form.get("idGrado")
    id_nivel =  request.form.get("idNivel")
    punto_inicial = request.form.get("PuntoInicial")
    punto_final = request.form.get("PuntoFinal")
    sueldo_base = request.form.get("SueldoBase")
    compensacion_garantizada = request.form.get("CompensacionGarantizada")
    datos = {
        "idAnioFiscal": anio_fiscal,
        "idGrupo": id_grupo,
        "idGrado": id_grado,
        "idNivel": id_nivel,
        "PuntoInicial": punto_inicial,
        "PuntoFinal": punto_final,
        "SueldoBase": sueldo_base,
        "CompensacionGarantizada": compensacion_garantizada,
    }
    tabme = db.session.query(rTabuladorSalarial).filter_by(idAnioFiscal = anio_fiscal, idGrupo = id_grupo, idGrado = id_grado, idNivel = id_nivel).first()
    if tabme:
        tabme.update(**datos)
        db.session.commit()
        actualizar_sueldos_puestos(anio_fiscal,id_grupo,id_grado,id_nivel)
        respuesta = 0
    else:
        respuesta = 1
    return jsonify({"respuesta": respuesta})

def actualizar_sueldos_puestos(anio_fiscal,id_grupo,id_grado,id_nivel):
    tabulador = db.session.query(rTabuladorSalarial).filter_by(idAnioFiscal = anio_fiscal, idGrupo = id_grupo, idGrado = id_grado, idNivel = id_nivel).first()
    if tabulador: 
        puestos = db.session.query(tPuesto).filter_by(idGrupo = id_grupo, idGrado = id_grado, idNivel = id_nivel).all()
        if puestos:
            for puesto in puestos:
                puesto.update(SueldoBase = tabulador.SueldoBase,Compensacion = tabulador.CompensacionGarantizada)
                db.session.commit()
            nivelpuesto = str(id_grupo) +""+ str(id_grado) + "" + str(id_nivel)
            empleadospuestos = db.session.query(rEmpleadoPuesto).filter_by(idNivel = nivelpuesto, idEstatusEP = 1).all()
            for empleadopuesto in empleadospuestos:
                empleadoconeptos = db.session.query(rEmpleadoConcepto).filter_by(idPersona = empleadopuesto.idPersona).all()
                if empleadoconeptos:
                    for empleadoconcepto in empleadoconeptos:
                        if empleadoconcepto.idConcepto == "7":
                            empleadoconcepto.Monto = tabulador.SueldoBase
                            db.session.commit()
                        if empleadoconcepto.idConcepto == "CG":
                            empleadoconcepto.Monto = tabulador.CompensacionGarantizada
                            db.session.commit()
    else:
        print("Sin registros")