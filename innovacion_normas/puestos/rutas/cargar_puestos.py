from .puestos import puestos
from flask import render_template, request, session, jsonify
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, func, inspect
from datetime import datetime, time
import openpyxl

from app import db
from rh.gestion_empleados.modelos.empleado import tPuesto
from catalogos.modelos.modelos import kEstatusPuesto, kVigencia, kCentroTrabajo

@puestos.route("/innovacion-normas/puestos/cargar-puestos", methods = ["POST", "GET"])
def cargar_puestos():

    return render_template("/cargar_puestos.html", title = "Cargar puestos")

@puestos.route("/innovacion-normas/puestos/cargar-archivo-puestos", methods = ["POST"])
def cargar_archivo_puestos():
    archivo = request.files.get("archivo")

    columnas = inspect(tPuesto).all_orm_descriptors.keys()
    del columnas[32:44]

    valor_columnas =[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 32, 41, 40]
    mapeo_nombres = dict(zip(columnas, valor_columnas))

    if(archivo):
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active

        datos_lista = []
        datos_dict = {}
        nuevo_puesto = None

        #idEstatusPuesto, idVigencia, idCentroTrabajo

        for row_value in range(12, ws.max_row + 1):
            for key in mapeo_nombres:
                datos_dict.update({key: ws.cell(row = row_value, column = mapeo_nombres[key]).value})
                if key == "idEstatusPuesto":
                    valor = db.session.query(kEstatusPuesto).filter_by(EstatusPuesto = datos_dict["idEstatusPuesto"]).one()
                    datos_dict["idEstatusPuesto"] = valor.idEstatusPuesto
                
                if key == "idVigencia":
                    valor = db.session.query(kVigencia).filter_by(Vigencia = datos_dict["idVigencia"]).one()
                    datos_dict["idVigencia"] = valor.idVigencia

                if key == "idCentroTrabajo":
                    valor = db.session.query(kCentroTrabajo).filter_by(CentroTrabajo = datos_dict["idCentroTrabajo"]).one()
                    datos_dict["idCentroTrabajo"] = valor.idCentroTrabajo

            datos_lista.append(datos_dict)

            try:
                puesto_existente = db.session.query(tPuesto).filter_by(ConsecutivoPuesto = datos_dict["ConsecutivoPuesto"]).one()
                puesto_existente.update(**datos_dict)

            except NoResultFound:
                nuevo_puesto = tPuesto(**datos_dict)
                db.session.add(nuevo_puesto)

        db.session.commit()


        return({"guardado": True})
    
    else:
        return({"guardado": False})