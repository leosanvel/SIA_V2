from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from general.herramientas.funciones import permisos_de_consulta
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user
from app import db



moduloSIA = Blueprint('principal', __name__, template_folder = '../plantillas', static_folder='../estatico', static_url_path='/principal/estatico') #por ej. 

@moduloSIA.route('/principal/sia')
@permisos_de_consulta
def sia():
    # try:
    #     empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    # except NoResultFound:
    #     empleado = None
    empleado = None
    return render_template('/SIA.html', title ='Sistema Integral Administrativo',
                            current_user=current_user,
                            empleado = empleado)








from autenticacion.modelos.modelos import Concepto, TipoConcepto, TipoPago, EmpleadoConcepto

@moduloSIA.route('/conceptos')
@permisos_de_consulta
def conceptos():
    # try:
    #     empleado = db.session.query(Empleados).filter_by(idPersona=current_user.idPersona, Activo=1).one()
    # except NoResultFound:
    #     empleado = None
    TiposConcepto = db.session.query(TipoConcepto).all()
    TiposPago = db.session.query(TipoPago).all()
    return render_template('/conceptos.html', title ='Conceptos',
                            current_user=current_user,
                            TipoConcepto = TiposConcepto,
                            TipoPago = TiposPago)


@moduloSIA.route('/crear-concepto', methods = ['POST'])
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
        concepto_a_modificar = db.session.query(Concepto).filter_by(idTipoConcepto = TipoConcepto, idConcepto = idConcepto).one()
        print("Ya existe")
    except NoResultFound:
        nuevo_concepto = Concepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@moduloSIA.route('/buscar-concepto', methods = ['POST'])
def concepto():
    tipoConcepto = request.form.get('TipoConcepto')
    concepto = request.form.get('Concepto')

    query = db.session.query(Concepto)
    
    if tipoConcepto != "0":
        query = query.filter(Concepto.idTipoConcepto == tipoConcepto)
    if concepto:
        query = query.filter(Concepto.Concepto.contains(concepto))
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


@moduloSIA.route('/empleado-conceptos')
@permisos_de_consulta
def empleado_conceptos():
    tiposConcepto = db.session.query(TipoConcepto).all()
    return render_template('/empleado_conceptos.html', title ='Empleado Conceptos',
                            current_user=current_user,
                            TipoConcepto = tiposConcepto)