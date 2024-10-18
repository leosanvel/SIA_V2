from flask import render_template, request, jsonify, session
from sqlalchemy import or_, cast, String, func
from datetime import date

from app import db
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
from general.herramientas.funciones import revision_baja_empleados
from rh.gestion_empleados.rutas.agregar_empleado import guardar_conceptos

@gestion_empleados.route('/rh/gestion-empleados/baja-alta-masiva-honorarios', methods = ['GET', 'POST'])
def alta_masiva_honorarios():
    Empleados_Honorarios_Inactivos = db.session.query(rEmpleadoPuesto).join(rEmpleado).join(tPersona).filter(rEmpleado.idTipoEmpleado == 1).order_by(tPersona.Nombre).all()

    return render_template('/alta_masivo_honorarios.html', title = 'Baja/Alta masiva honorarios',
                           Empleados_Honorarios_Inactivos = Empleados_Honorarios_Inactivos)

@gestion_empleados.route('/rh/gestion-empleados/buscar-empleados-honorarios', methods = ['GET', 'POST'])
def buscar_empleados_honorarios_inactivos():

    #Empleados_Honorarios_Inactivos = db.session.query(rEmpleadoPuesto).join(rEmpleado).join(tPersona).filter(rEmpleado.idTipoEmpleado == 1).order_by(tPersona.Nombre).all()

    # Subconsulta para obtener el idPersona con la FechaInicio más reciente
    subquery = (
        db.session.query(
            rEmpleadoPuesto.idPersona,
            func.max(rEmpleadoPuesto.FechaInicio).label('max_fecha_inicio')
        )
        .group_by(rEmpleadoPuesto.idPersona)
        .subquery()
    )

    # Consulta principal que une la subconsulta con rEmpleadoPuesto
    Empleados_Honorarios = (
        db.session.query(rEmpleadoPuesto)
        .join(subquery, 
            (rEmpleadoPuesto.idPersona == subquery.c.idPersona) & 
            (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio))
        .join(rEmpleado)
        .join(tPersona)
        .filter(rEmpleado.idTipoEmpleado == 1)
        .order_by(tPersona.Nombre)
        .all()
    )

    lista_empleados = []
    empleado_data = {}

    for Empleado in Empleados_Honorarios:
        if Empleado.Empleado.Persona:
            empleado_data["Nombre"] = Empleado.Empleado.Persona.Nombre + ' ' + Empleado.Empleado.Persona.ApPaterno + ' ' + Empleado.Empleado.Persona.ApMaterno

        empleado_data["NumEmpleado"] = Empleado.Empleado.NumeroEmpleado
        empleado_data["idPersona"] = Empleado.idPersona
        #print(empleado_data)

        lista_empleados.append(empleado_data.copy())
    
    return jsonify(lista_empleados)

@gestion_empleados.route("/rh/gestion-empleados/generar-bajas-altas-masivo-honorarios", methods = ["GET", "POST"])
def generar_altas_bajas_masivo_honorarios():
    datos = request.get_json()

    if "ListaEmpleados" in datos:
        ListaEmpleados = datos["ListaEmpleados"]

    print(ListaEmpleados)
    hoy = date.today()
    print(hoy)
    quincena = db.session.query(kQuincena).filter(
        kQuincena.FechaInicio <= hoy,
        kQuincena.FechaFin >= hoy
    ).first()

    if quincena is not None:
        NumQuincena = quincena.idQuincena
    else:
        NumQuincena = None

    print(quincena)

    for idPersona in ListaEmpleados:
        reg_EmpleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == int(idPersona)).order_by(rEmpleadoPuesto.FechaInicio.desc()).first()

        print(reg_EmpleadoPuesto)

        if reg_EmpleadoPuesto is not None:
            if reg_EmpleadoPuesto.idEstatusEP == 1:
                
                reg_EmpleadoPuesto.idCausaBaja = 8
                reg_EmpleadoPuesto.Observaciones = "Termino de contrato"
                reg_EmpleadoPuesto.FechaEfecto = hoy
                reg_EmpleadoPuesto.idQuincena = NumQuincena
                reg_EmpleadoPuesto.ConservaVacaciones = 0

                db.session.commit()

                if reg_EmpleadoPuesto.FechaEfecto == hoy:
                    print(reg_EmpleadoPuesto.__dict__)
                    revision_baja_empleados(idPersona = idPersona, hoy = reg_EmpleadoPuesto.FechaEfecto)

        EmpleadoPuesto_data = {
            "idPersona": reg_EmpleadoPuesto.idPersona,
            "idPuesto": reg_EmpleadoPuesto.idPuesto,
            "CodigoPuesto": reg_EmpleadoPuesto.CodigoPuesto,
            "ClavePresupuestaSIA": reg_EmpleadoPuesto.ClavePresupuestaSIA,
            "CodigoPlazaSIA": reg_EmpleadoPuesto.CodigoPlazaSia,
            "CodigoPuestoSIA": reg_EmpleadoPuesto.CodigoPuestoSIA,
            "RHNETSIA": reg_EmpleadoPuesto.RHNETSIA,
            "idNivel": reg_EmpleadoPuesto.idNivel,
            "idCentroCosto": reg_EmpleadoPuesto.idCentroCosto,
            "idUbicacion": reg_EmpleadoPuesto.idUbicacion,
            "FechaInicio": hoy,
            "FechaTermino": None,
            "idCausaBaja": None,
            "Observaciones": None,
            "FechaEfecto": None,
            "idQuincena": None,
            "ConservaVacaciones": None,
            "idEstatusEP": 1
        }
        print(EmpleadoPuesto_data)

        nuevo_EmpleadoPuesto = rEmpleadoPuesto(**EmpleadoPuesto_data)
        db.session.add(nuevo_EmpleadoPuesto)

        reg_EmpleadoPuesto.Empleado.Activo = 1

        db.session.commit()

        if nuevo_EmpleadoPuesto is not None:
            session["idPersona"] = nuevo_EmpleadoPuesto.idPersona

        guardar_conceptos()


    return jsonify({'respuesta': True})