from flask import render_template, request, jsonify, session
from flask_login import current_user
from sqlalchemy import or_, cast, String, func, and_, desc
from datetime import date

from app import db
from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
from general.herramientas.funciones import revision_baja_empleados
from rh.gestion_empleados.rutas.agregar_empleado import guardar_conceptos
from general.modelos.modelos import tBitacora

@gestion_empleados.route('/rh/gestion-empleados/baja-alta-masiva-honorarios', methods = ['GET', 'POST'])
def alta_masiva_honorarios():
    Empleados_Honorarios_Inactivos = db.session.query(rEmpleadoPuesto).join(rEmpleado).join(tPersona).filter(rEmpleado.idTipoEmpleado == 1).order_by(tPersona.Nombre).all()

    return render_template('/alta_masivo_honorarios.html', title = 'Baja/Alta masiva honorarios',
                           Empleados_Honorarios_Inactivos = Empleados_Honorarios_Inactivos)

@gestion_empleados.route('/rh/gestion-empleados/buscar-empleados-honorarios', methods = ['GET', 'POST'])
def buscar_empleados_honorarios_inactivos():

    Busqueda = request.form.get("Busqueda")
    Opcion = request.form.get("Opcion")

    # Subconsulta para obtener el idPersona con la FechaInicio más reciente
    subquery = (
        db.session.query(
            rEmpleadoPuesto.idPersona,
            func.max(rEmpleadoPuesto.FechaInicio).label('max_fecha_inicio')
        )
        .group_by(rEmpleadoPuesto.idPersona)
        .subquery()
    )

    if Opcion == "1":
        # Consulta principal que une la subconsulta con rEmpleadoPuesto
        Empleados_Honorarios = (
            db.session.query(rEmpleadoPuesto)
            .join(subquery, 
                (rEmpleadoPuesto.idPersona == subquery.c.idPersona) & 
                (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio), isouter=False
            )
            .join(rEmpleado, rEmpleado.idPersona == rEmpleadoPuesto.idPersona, isouter=False)
            .join(tPersona, tPersona.idPersona == rEmpleado.idPersona, isouter=False)
            .filter(
                rEmpleado.Activo == 1,
                rEmpleado.idTipoEmpleado == 1,
                rEmpleadoPuesto.idEstatusEP == 1,
                or_(
                    tPersona.Nombre.contains(Busqueda),
                    tPersona.ApPaterno.contains(Busqueda),
                    tPersona.ApMaterno.contains(Busqueda),
                    rEmpleado.NumeroEmpleado.contains(Busqueda)
                )  
            )
            .order_by(tPersona.Nombre)
            .all()
        )

    else:
        Empleados_Honorarios = (
            db.session.query(rEmpleadoPuesto)
            .join(rEmpleado, rEmpleado.idPersona == rEmpleadoPuesto.idPersona)
            .join(tPersona, tPersona.idPersona == rEmpleado.idPersona)
            #.join(kCentroCostos, kCentroCostos.idCentroCosto == rEmpleadoPuesto.idCentroCosto)
            .join(rEmpleadoContrato, rEmpleadoContrato.idPersona == rEmpleadoPuesto.idPersona)
            .join(subquery, 
                (rEmpleadoPuesto.idPersona == subquery.c.idPersona) & 
                (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio), isouter=False
            )
            .filter(
                rEmpleadoContrato.FechaFin < date.today(),
                or_(
                    tPersona.Nombre.ilike(f"%{Busqueda}%"),
                    tPersona.ApPaterno.ilike(f"%{Busqueda}%"),
                    tPersona.ApMaterno.ilike(f"%{Busqueda}%"),
                    rEmpleado.NumeroEmpleado.ilike(f"%{Busqueda}%"),
                    #kCentroCostos.CentroCosto.ilike(f"%{Busqueda}%"),
                    #kCentroCostos.Clave.ilike(f"%{Busqueda}%")
                )
            )
            .order_by(tPersona.Nombre)
        ).all()

    if len(Empleados_Honorarios) == 0:
        resultado_centro_costos = (
            db.session.query(kCentroCostos)
            .filter(
                or_(
                    kCentroCostos.CentroCosto.contains(Busqueda),
                    kCentroCostos.Clave.contains(Busqueda)
                )
            ).all()
        )

        Empleados_Honorarios = []

        for centro_costo in resultado_centro_costos:
            if Opcion == "1":
                Empleados_Honorarios.extend(
                    db.session.query(rEmpleadoPuesto)
                    .join(subquery, 
                        (rEmpleadoPuesto.idPersona == subquery.c.idPersona) & 
                        (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio)
                    )
                    .join(rEmpleado)
                    .join(tPersona)
                    .filter(rEmpleadoPuesto.idCentroCosto == centro_costo.idCentroCosto, rEmpleado.idTipoEmpleado == 1,         rEmpleado.Activo == 1)
                    .order_by(tPersona.Nombre)
                    .all()
                )

            else:
                Empleados_Honorarios.extend(
                    db.session.query(rEmpleadoPuesto)
                    .join(subquery, 
                        (rEmpleadoPuesto.idPersona == subquery.c.idPersona) & 
                        (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio)
                    )
                    .join(rEmpleado)
                    .join(tPersona)
                    .join(rEmpleadoContrato, rEmpleadoContrato.idPersona == rEmpleadoPuesto.idPersona)
                    .filter(
                        rEmpleadoPuesto.idCentroCosto == centro_costo.idCentroCosto,
                        rEmpleado.idTipoEmpleado == 1,
                        rEmpleadoContrato.FechaFin < date.today(),
                        rEmpleado.Activo == 1)
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
        
        centro_costo = db.session.query(kCentroCostos).filter_by(idCentroCosto = Empleado.idCentroCosto).first()
        empleado_data["CentroCosto"] = centro_costo.Clave

        lista_empleados.append(empleado_data.copy())
    
    return jsonify(lista_empleados)

@gestion_empleados.route("/rh/gestion-empleados/generar-bajas-altas-masivo-honorarios", methods = ["GET", "POST"])
def generar_altas_bajas_masivo_honorarios():
    datos = request.get_json()

    opcion = datos["Opcion"]
    
    FechaInicio = datos["FechaInicio"]
    FechaFin = datos["FechaFin"]

    if FechaInicio != "":
        FechaInicio = datetime.strptime(FechaInicio, '%d/%m/%Y')
    if FechaFin != "":
        FechaFin = datetime.strptime(FechaFin, '%d/%m/%Y')

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

    for idPersona in ListaEmpleados:
        reg_EmpleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idPersona == int(idPersona)).order_by(rEmpleadoPuesto.FechaInicio.desc()).first()

        print(reg_EmpleadoPuesto)

        if opcion == "1" or opcion == "2":
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
                        TipoMovimiento = 3
                        # Calcular último id guardado para el movimiento de baja de empleado
                        ultimo_id_movimiento = db.session.query(func.max(rMovimientoEmpleado.idMovimientoEmpleado)).filter_by(idTipoMovimiento=TipoMovimiento).scalar()
                        if ultimo_id_movimiento is None:
                            idMovimientoEmpleado = 1
                        else:
                            idMovimientoEmpleado = ultimo_id_movimiento + 1

                        # Calcular último id guardado para la bitacora de baja de empleado
                        ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
                        if ultimo_idBitacora is None:
                            idBitacora = 1
                        else:
                            idBitacora = ultimo_idBitacora + 1

                        Periodo = datetime.now().year

                        nuevo_movimiento = rMovimientoEmpleado(idMovimientoEmpleado=idMovimientoEmpleado,
                                                               idTipoMovimiento=3,
                                                               idPersonaMod=idPersona,
                                                               idTipoEmpleado=1,
                                                               idUsuario=current_user.idPersona,
                                                               idQuincena=NumQuincena,
                                                               Periodo=Periodo)
        
                        db.session.add(nuevo_movimiento)
        
                        nueva_bitacora = tBitacora(idBitacora=idBitacora,
                                                   idTipoMovimiento=3,
                                                   idUsuario=current_user.idPersona)
        
                        db.session.add(nueva_bitacora)

        if opcion == "1":
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
                "FechaInicio": FechaInicio,
                "FechaTermino": FechaFin,
                "idCausaBaja": None,
                "Observaciones": None,
                "FechaEfecto": None,
                "idQuincena": None,
                "ConservaVacaciones": None,
                "idEstatusEP": 1
            }

            if FechaInicio > FechaFin:
                FechaInicio, FechaFin = FechaFin, FechaInicio

            anios_dif = FechaFin.year - FechaInicio.year
            mes_dif = FechaFin.month - FechaInicio.month

            meses_totales = (anios_dif*12) + mes_dif + 1

            print(meses_totales)

            ultimo_contrato = db.session.query(rEmpleadoContrato).filter(
                rEmpleadoContrato.idPersona == reg_EmpleadoPuesto.idPersona,
                rEmpleadoContrato.FechaInicio <= hoy,
                rEmpleadoContrato.FechaFin < hoy).order_by(desc(rEmpleadoContrato.FechaInicio)).first()
            
            print(ultimo_contrato)

            columnas_excluir = {'idPersona','FechaInicio', 'FechaFin', 'NumeroExhibicion'}
            if ultimo_contrato is not None:
                nuevo_contrato = {columna.name: getattr(ultimo_contrato, columna.name)
                                  for columna in rEmpleadoContrato.__table__.columns
                                  if columna.name not in columnas_excluir}
            else:
                nuevo_contrato = {}
                for columna in rEmpleadoContrato.__table__.columns:
                    if columna.name not in columnas_excluir:
                        if isinstance(columna.type, db.String):
                            nuevo_contrato[columna.name] = ""
                        elif isinstance(columna.type, db.Numeric):
                            nuevo_contrato[columna.name] = 0.0
                        elif isinstance(columna.type, db.Integer):
                            nuevo_contrato[columna.name] = 0
                        else:
                            nuevo_contrato[columna.name] = None
                
            nuevo_contrato["idPersona"] = reg_EmpleadoPuesto.idPersona
            nuevo_contrato["AnioFiscal"] = FechaInicio.year
            nuevo_contrato["FechaInicio"] = FechaInicio
            nuevo_contrato["FechaFin"] = FechaFin
            nuevo_contrato["FechaFirma"] = FechaInicio
            nuevo_contrato["NumeroExhibicion"] = meses_totales
            nuevo_contrato["ImporteBruto"] = meses_totales*nuevo_contrato["MontoPactado"]
            nuevo_contrato["ContratoGenerado"] = 0

            ultimo_NumeroContrato = db.session.query(func.max(rEmpleadoContrato.NumeroContrato)).filter_by(idPersona = nuevo_contrato["idPersona"]).scalar()
            if ultimo_NumeroContrato is None:
                nuevo_contrato["NumeroContrato"] = 1
            else:
                nuevo_contrato["NumeroContrato"] = ultimo_NumeroContrato + 1

            print(nuevo_contrato)

            nuevo_EmpleadoContrato = rEmpleadoContrato(**nuevo_contrato)
            db.session.add(nuevo_EmpleadoContrato)

            nuevo_EmpleadoPuesto = rEmpleadoPuesto(**EmpleadoPuesto_data)
            db.session.add(nuevo_EmpleadoPuesto)

            reg_EmpleadoPuesto.Empleado.Activo = 1

            TipoMovimiento = 1

            # Calcular último id guardado para el movimiento de baja de empleado
            ultimo_id_movimiento = db.session.query(func.max(rMovimientoEmpleado.idMovimientoEmpleado)).filter_by(idTipoMovimiento=TipoMovimiento).scalar()
            if ultimo_id_movimiento is None:
                idMovimientoEmpleado = 1
            else:
                idMovimientoEmpleado = ultimo_id_movimiento + 1

            # Calcular último id guardado para la bitacora de baja de empleado
            ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
            if ultimo_idBitacora is None:
                idBitacora = 1
            else:
                idBitacora = ultimo_idBitacora + 1
            Periodo = datetime.now().year
            nuevo_movimiento = rMovimientoEmpleado(idMovimientoEmpleado=idMovimientoEmpleado,
                                                   idTipoMovimiento=1,
                                                   idPersonaMod=idPersona,
                                                   idTipoEmpleado=1,
                                                   idUsuario=current_user.idPersona,
                                                   idQuincena=NumQuincena,
                                                   Periodo=Periodo)
        
            db.session.add(nuevo_movimiento)
        
            nueva_bitacora = tBitacora(idBitacora=idBitacora,
                                       idTipoMovimiento=1,
                                       idUsuario=current_user.idPersona)
        
            db.session.add(nueva_bitacora)
            
        db.session.commit()


        # # Calcular último id guardado para el movimiento de baja de empleado
        # ultimo_id_movimiento = db.session.query(func.max(rMovimientoEmpleado.idMovimientoEmpleado)).filter_by(idTipoMovimiento=TipoMovimiento).scalar()
        # if ultimo_id_movimiento is None:
        #     idMovimientoEmpleado = 1
        # else:
        #     idMovimientoEmpleado = ultimo_id_movimiento + 1

        # # Calcular último id guardado para la bitacora de baja de empleado
        # ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
        # if ultimo_idBitacora is None:
        #     idBitacora = 1
        # else:
        #     idBitacora = ultimo_idBitacora + 1

        # Periodo = datetime.now().year

        # nuevo_movimiento = rMovimientoEmpleado(idMovimientoEmpleado=idMovimientoEmpleado,
        #                                        idTipoMovimiento=TipoMovimiento,
        #                                        idPersonaMod=idPersona,
        #                                        idTipoEmpleado=1,
        #                                        idUsuario=current_user.idPersona,
        #                                        idQuincena=NumQuincena,
        #                                        Periodo=Periodo)
        
        # db.session.add(nuevo_movimiento)
        
        # nueva_bitacora = tBitacora(idBitacora=idBitacora,
        #                        idTipoMovimiento=TipoMovimiento,
        #                        idUsuario=current_user.idPersona)
        
        # db.session.add(nueva_bitacora)

    return jsonify({'respuesta': True})