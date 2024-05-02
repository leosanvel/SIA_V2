from .rutas import catalogos
from flask import render_template, request, jsonify
from flask_login import current_user

from app import db
from catalogos.modelos.modelos import kConcepto, kTipoConcepto, kTipoPago
from sqlalchemy.orm.exc import NoResultFound

@catalogos.route('/catalogos/conceptos')
def catalogos_conceptos():
    TiposConcepto = db.session.query(kTipoConcepto).all()
    TiposPago = db.session.query(kTipoPago).all()
    return render_template('/conceptos.html', title ='Conceptos',
                            current_user=current_user,
                            TipoConcepto = TiposConcepto,
                            TipoPago = TiposPago)


@catalogos.route('/catalogos/crear-concepto', methods = ['POST'])
def crear_concepto():
    TipoConcepto = request.form['TipoConcepto']
    idConcepto = request.form['idConcepto']

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

    except NoResultFound:
        nuevo_concepto = kConcepto(**concepto_data)
        db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()
       
    return jsonify(concepto_data)

@catalogos.route('/catalogos/buscar-concepto', methods = ['POST'])
def concepto():
    respuesta = {}
    concepto = request.form.get('ConceptoExistente')
    if concepto:
        query = db.session.query(kConcepto)
    
        partes = concepto.split(' - ')
        
        if len(partes) == 3:
            query = query.filter(kConcepto.idTipoConcepto == partes[0])
            query = query.filter(kConcepto.idConcepto == partes[1])
            query = query.filter(kConcepto.Concepto.contains(partes[2]))
        else:
            query = query.filter(kConcepto.Concepto.contains(concepto))
        conceptos = query.all()
    else:
        conceptos = []


    lista_conceptos = []
    for conc in conceptos:
        if conc is not None:
            conc_dict = conc.__dict__
            conc_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_conceptos.append(conc_dict)
    if not lista_conceptos:
        respuesta["NoEncontrado"] = True

    tipospago = db.session.query(kTipoPago).all()
    lista_tipo_pago = []
    for tipopago in tipospago:
        if tipopago is not None:
            tipopago_dict = tipopago.__dict__
            tipopago_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_tipo_pago.append(tipopago_dict)

        
    respuesta["ListaConceptos"] = lista_conceptos   
    respuesta["TipoPago"] = lista_tipo_pago   
 

    return jsonify(respuesta)

@catalogos.route('/catalogos/actualizar-busqueda-conceptos', methods=['GET'])
def actualizar_busqueda_conceptos():
    texto_busqueda = request.args.get('texto_busqueda', '')
    resultados = kConcepto.query.filter(kConcepto.Concepto.ilike(f'%{texto_busqueda}%')).all()
    resultados_json = [{'idTipoConcepto': resultado.idTipoConcepto,
                        'idConcepto': resultado.idConcepto,
                        'Concepto': resultado.Concepto,
                        'Abreviatura': resultado.Abreviatura,
                        'Porcentaje': resultado.Porcentaje,
                        'Monto': resultado.Monto,
                        'ClaveSAT': resultado.ClaveSAT,
                        'idTipoPago': resultado.idTipoPago,
                        'Activo': resultado.Activo,
                        'texto': str(resultado.idTipoConcepto) + ' - ' + str(resultado.idConcepto) + ' - ' + str(resultado.Concepto)
                        } for resultado in resultados]
    return jsonify(resultados_json)


@catalogos.route('/catalogos/cancela_casdoncepto', methods = ['POST', 'GET'])
def cancelasda_concepto():
    idIncidencia = request.form.get('idIncidencia')
    Incidencia = db.session.query(Tincidencia).filter_by(idIncidencia = idIncidencia).first()
    if Incidencia is not None:
        Incidencia_dict = Incidencia.__dict__
        Incidencia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(Incidencia_dict)
    else:
        return jsonify(False)