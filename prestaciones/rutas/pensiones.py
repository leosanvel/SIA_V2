from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user
from sqlalchemy import func, inspect

from app import db
from prestaciones.modelos.modelos import rEmpleadoPensiones
from rh.gestion_empleados.modelos.empleado import rEmpleado

@prestaciones.route('/prestaciones/pensiones', methods = ['GET', 'POST'])
def pensiones():
    
    return render_template('/pensiones.html', title = "Pensiones")

@prestaciones.route('/prestaciones/pensiones/buscar-pensiones', methods = ["POST"])
def buscar_pensiones():
    idPersona = request.form.get("idPersona")
    print(idPersona)

    pensiones = db.session.query(rEmpleadoPensiones).filter_by(idPersona = idPersona).all()

    print(pensiones)

    lista_pensiones = []

    for pension in pensiones:
        if pension is not None:
            Empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
            if Empleado is not None:
                Nombre = Empleado.Persona.ApPaterno + " " + Empleado.Persona.ApMaterno + " " + Empleado.Persona.Nombre
                NumeroEmpleado = Empleado.NumeroEmpleado
            else:
                Nombre = ""
                NumeroEmpleado = ""
            pensiones_dict = pension.__dict__
            pensiones_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            pensiones_dict["Nombre"] = Nombre
            pensiones_dict["NumeroEmpleado"] = NumeroEmpleado

            lista_pensiones.append(pensiones_dict)

    print(lista_pensiones)

    return jsonify({"pensiones": lista_pensiones})

@prestaciones.route('/prestaciones/pensiones/guardar-pension', methods = ["POST"])
def guardar_pensiones():
    respuesta = 0

    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'NombreBeneficiario': 'NombreBeneficiario',
        'RFC': 'RFC',
        'ClabeBancaria': 'ClabeBancaria',
        'Observaciones': 'Observaciones',
        'idPersona': 'idPersona'
    }

    pension_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    pension_existente = db.session.query(rEmpleadoPensiones).filter_by(idPersona = pension_data["idPersona"], NombreBeneficiario = pension_data["NombreBeneficiario"]).first()

    if pension_existente is None:
        ultimo_idEmpleadoPension = db.session.query(func.max(rEmpleadoPensiones.idEmpleadoPensiones)).scalar()
        if ultimo_idEmpleadoPension is None:
            pension_data["idEmpleadoPensiones"] = 1
        else:
            pension_data["idEmpleadoPensiones"] = ultimo_idEmpleadoPension + 1

        nueva_pension = rEmpleadoPensiones(**pension_data)
        db.session.add(nueva_pension)

        db.session.commit()
        estado = inspect(nueva_pension)
        if estado.persistent:
            respuesta = 99
        else:
            respuesta = 2
    
    else:
        respuesta = 1

    return jsonify({"respuesta": respuesta})