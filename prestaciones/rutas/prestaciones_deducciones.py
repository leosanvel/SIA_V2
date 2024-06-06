from .rutas import prestaciones
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from prestaciones.modelos.modelos import rEmpleadoConcepto, rEmpleadoSueldo
from rh.gestion_empleados.modelos.empleado import rEmpleado
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from datetime import datetime

@prestaciones.route('/prestaciones/prestaciones-deducciones')
def empleado_conceptos():
    tiposConcepto = db.session.query(kTipoConcepto).all()
    return render_template('/prestaciones_deducciones.html', title ='Prestaciones y deducciones',
                            current_user=current_user,
                            TipoConcepto = tiposConcepto)

@prestaciones.route('/prestaciones/crear-empleado-concepto', methods = ['POST'])
def crear_empleado_concepto():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona' : 'idPersona',
        'TipoConcepto' : 'idTipoConcepto',
        'Concepto' : 'idConcepto',
        'Porcentaje' : 'Porcentaje',
        'Monto' : 'Monto',
        'NumeroContrato': 'NumeroContrato',
        'FechaInicioContrato': 'FechaInicio',
        'FechaFinContrato': 'FechaFin',
        'PagoUnico': 'PagoUnico'
    }
    concepto_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    if concepto_data['NumeroContrato'] is None:
        concepto_data['NumeroContrato'] = 1
    else:
        # Convertir la fecha a un objeto datetime
        fecha_inicio_dt = datetime.strptime(concepto_data['FechaInicio'], '%d/%m/%Y')
        fecha_fin_dt = datetime.strptime(concepto_data['FechaFin'], '%d/%m/%Y')

        # Formatear la fecha en el formato 'YYYY-MM-DD'
        concepto_data['FechaInicio'] = fecha_inicio_dt.strftime('%Y-%m-%d')
        concepto_data['FechaFin'] = fecha_fin_dt.strftime('%Y-%m-%d')
    concepto_data['PagoUnico'] = 0

    editar = request.form.get('editar')
    contrato = request.form.get('checkboxContrato')
    
    idPersona = concepto_data.get('idPersona', None)
    idTipoConcepto = concepto_data.get('idTipoConcepto', None)
    idConcepto = concepto_data.get('idConcepto', None)
    NumeroContrato = concepto_data.get('NumeroContrato', None)

    nuevo_concepto = None
    try:
        concepto_a_modificar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto, NumeroContrato = NumeroContrato).one()
        if editar == "true":
            concepto_a_modificar.update(**concepto_data)
            print("concepto modificado")
        else:
            print("Ya existía")
            return jsonify({'Existente':True})

    except NoResultFound:
        nuevo_concepto = rEmpleadoConcepto(**concepto_data)
        print("Nuevo concepto")
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@prestaciones.route('/prestaciones/buscar-empleado-concepto', methods = ['POST'])
def buscar_empleado_concepto():
    idPersona = request.form.get('idPersona')
    empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
    empleadoConceptos = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona).all()
    print("El número de conceptos encontrados es: " + str(len(empleadoConceptos)))

    lista_empleado_conceptos = []
    for emp_con in empleadoConceptos:
        concepto = db.session.query(kConcepto).filter_by(idConcepto = emp_con.idConcepto, idTipoConcepto = emp_con.idTipoConcepto).first()
        if emp_con is not None:
            emp_con_dict = emp_con.__dict__
            emp_con_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            emp_con_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
            emp_con_dict["Concepto"] = concepto.Concepto
            lista_empleado_conceptos.append(emp_con_dict)
    if not lista_empleado_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_empleado_conceptos)


@prestaciones.route('/prestaciones/filtrar-conceptos', methods = ['POST'])
def filtrar_concepto():

    datos = request.get_json()
    TipoConcepto = datos.pop("TipoConcepto", None)
    idPersona = datos.pop("idPersona", None)
    BuscarRepetidos = datos.pop("BuscarRepetidos", None)
    conceptos = db.session.query(kConcepto).filter_by(idTipoConcepto=TipoConcepto).order_by(asc(kConcepto.Concepto)).all()

    lista_conceptos = []
    for concepto in conceptos:
        empleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idConcepto = concepto.idConcepto, idTipoConcepto = concepto.idTipoConcepto).first()

        if empleadoConcepto is None or BuscarRepetidos=="true":

            if concepto is not None:
                concepto_dict = concepto.__dict__
                concepto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                lista_conceptos.append(concepto_dict)
    if not lista_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_conceptos)



@prestaciones.route('/prestaciones/obtener-concepto', methods = ['POST'])
def obtener_concepto():

    TipoConcepto = request.form.get('TipoConcepto')
    Concepto = request.form.get('Concepto')

    conceptos = db.session.query(kConcepto).filter_by(idTipoConcepto=TipoConcepto, idConcepto=Concepto).first()

    if conceptos is not None:
        concepto_dict = conceptos.__dict__
        concepto_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify({"concepto": concepto_dict,
                       "NoEncontrado":False},)

    else:
        return jsonify({"NoEncontrado":True}) 


@prestaciones.route('/prestaciones/eliminar-empleado-concepto', methods = ['POST'])
def eliminar_empleado_concepto():

    idPersona = request.form.get('idPersona')
    idTipoConcepto = request.form.get('TipoConcepto')
    idConcepto = request.form.get('Concepto')

    concepto_a_eliminar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto).delete()
    if concepto_a_eliminar > 0:
        print("El registro fue eliminado correctamente.")
    else:
        print("No se encontró ningún registro para eliminar.")
    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify({"eliminado":True})



@prestaciones.route('/prestaciones/carga-compensacion-sueldo', methods = ['POST'])
def cargr_compensacion_sueldo():

    datos = request.get_json()

    concepto = datos.get("concepto", None)
    idPersona = datos.get("idPersona", None)
    resultado = {}
    compensacion_sueldo = db.session.query(rEmpleadoSueldo).filter_by(idPersona = idPersona).one()
    if concepto == "7":
        resultado["Monto"] = compensacion_sueldo.Salario
        print("SALARIO")
    if concepto == "CG":
        resultado["Monto"] = compensacion_sueldo.Compensacion
        print("Compensacion")
    return jsonify(resultado)
       
    return jsonify({"eliminado":True})