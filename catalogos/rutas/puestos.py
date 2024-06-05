from .rutas import catalogos
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import inspect, or_
import pandas as pd

from app import db
from rh.gestion_empleados.modelos.empleado import tPuesto

@catalogos.route('/catalogos/puestos')
def catalogos_puestos():

    return render_template('/puestos.html', title = 'Puestos')

@catalogos.route("/catalogos/actualizar-busqueda-puestos", methods = ["GET"])
def actualizar_busqueda_puestos():
    texto_busqueda = request.args.get("texto_busqueda", "")
    resultados_json = []
    resultados = tPuesto.query.filter(or_(tPuesto.Puesto.ilike(f'%{texto_busqueda}%'), tPuesto.ConsPuesto.ilike(f'%{texto_busqueda}%'))).all()

    for resultado in resultados:
        if resultado is not None:
            resultado_dict = resultado.__dict__
            resultado_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            resultados_json.append(resultado_dict)

    return jsonify(resultados_json)

@catalogos.route("/catalogos/cargar_archivo_puestos", methods = ["POST"])
def cargar_archivo_puestos():
    archivo = request.files.get('archivo')
    #print(archivo)

    columnas = inspect(tPuesto).all_orm_descriptors.keys()

    df = pd.read_excel(archivo)

    #print(df.set_index(columnas).to_dict('records'))

    return({"guardado": True})