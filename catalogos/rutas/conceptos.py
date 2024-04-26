from .rutas import catalogos
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago, rEmpleadoConcepto
from sqlalchemy.orm.exc import NoResultFound

@catalogos.route('/catalogos/conceptos')
def catalogos_conceptos():
    print("HOLA")
    TiposConcepto = db.session.query(kTipoConcepto).all()
    TiposPago = db.session.query(kTipoPago).all()
    return render_template('/conceptos.html', title ='Conceptos',
                            current_user=current_user,
                            TipoConcepto = TiposConcepto,
                            TipoPago = TiposPago)


@catalogos.route('/crear-concepto', methods = ['POST'])
def crear_concepto():
    TipoConcepto = request.form['TipoConcepto']
    idConcepto = request.form['idConcepto']
    NuevoConcepto = request.form['Concepto']
    ClaveSAT = request.form['ClaveSAT']
    TipoPago = request.form['TipoPago']
    Porcentaje = request.form['Porcentaje']
    Monto = request.form['Monto']

    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'TipoConcepto' : 'idTipoConcepto',
        'idConcepto' : 'idConcepto',
        'Concepto' : 'Concepto',
        'Abreviatura' : 'Abreviatura',
        'ClaveSAT' : 'ClaveSAT',
        'TipoPago' : 'idTipoPago',
        'Porcentaje' : 'Porcentaje',
        'Monto' : 'Monto'
    }
    concepto_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    concepto_data["Activo"] = 1
    nuevo_concepto = None
    try:
        concepto_a_modificar = db.session.query(kConcepto).filter_by(idTipoConcepto = TipoConcepto, idConcepto = idConcepto).one()
        print("Ya existe")
    except NoResultFound:
        nuevo_concepto = kConcepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@catalogos.route('/buscar-concepto', methods = ['POST'])
def concepto():
    tipoConcepto = request.form.get('TipoConcepto')
    concepto = request.form.get('Concepto')

    query = db.session.query(kConcepto)
    
    if tipoConcepto != "0":
        query = query.filter(kConcepto.idTipoConcepto == tipoConcepto)
    if concepto:
        query = query.filter(kConcepto.Concepto.contains(concepto))
    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not concepto and tipoConcepto == "0":
        conceptos = []
    else:
        conceptos = query.all()


    lista_conceptos = []
    for conc in conceptos:
        if conc is not None:
            conc_dict = conc.__dict__
            conc_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_conceptos.append(conc_dict)
    if not lista_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_conceptos)


@catalogos.route('/prestaciones/empleado-concepto')
def empleado_conceptos():
    tiposConcepto = db.session.query(kTipoConcepto).all()
    return render_template('/empleado_conceptos.html', title ='Empleado Conceptos',
                            current_user=current_user,
                            TipoConcepto = tiposConcepto)

@catalogos.route('/crear-empleado-concepto', methods = ['POST'])
def crear_empleado_concepto():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idPersona' : 'idPersona',
        'TipoConcepto' : 'idTipoConcepto',
        'idConcepto' : 'idConcepto',
        'Porcentaje' : 'Porcentaje',
        'Monto' : 'Monto'
    }
    concepto_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}
    concepto_data['idPersona'] = 1
    print("concepto_data")
    print(concepto_data)

    idPersona = concepto_data.get('idPersona', None)
    idTipoConcepto = concepto_data.get('idTipoConcepto', None)
    idConcepto = concepto_data.get('idConcepto', None)
    nuevo_concepto = None
    try:
        concepto_a_modificar = db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = idTipoConcepto, idConcepto = idConcepto).one()
        print("Ya existe")
    except NoResultFound:
        nuevo_concepto = rEmpleadoConcepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@catalogos.route('/buscar-empleado-concepto', methods = ['POST'])
def buscar_empleado_concepto():
    idtipoConcepto = request.form.get('TipoConcepto')
    idconcepto = request.form.get('Concepto')
    idPersona = request.form.get('idPersona')

    query = db.session.query(rEmpleadoConcepto)

    if idPersona:
        query = query.filter(rEmpleadoConcepto.idPersona == idPersona)
    if idtipoConcepto != "0":
        query = query.filter(rEmpleadoConcepto.idTipoConcepto == idtipoConcepto)
    if concepto:
        query = query.filter(rEmpleadoConcepto.idConcepto.contains(idconcepto))
    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not concepto and idtipoConcepto == "0":
        empleadoConceptos = []
    else:
        empleadoConceptos = query.all()


    lista_empleado_conceptos = []
    for emp_con in empleadoConceptos:
        if emp_con is not None:
            emp_con_dict = emp_con.__dict__
            emp_con_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_empleado_conceptos.append(emp_con_dict)
    if not lista_empleado_conceptos:
        return jsonify({"NoEncontrado":True}) 
    return jsonify(lista_empleado_conceptos)