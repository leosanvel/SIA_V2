from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory, url_for
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
import os
from num2words import num2words

from .gestion_empleados import gestion_empleados
from app import db
from rh.gestion_empleados.modelos.empleado import rEmpleado, tPersona, rEmpleadoPuesto, tPuestoHonorarios, rEmpleadoContrato, rPersonaEscolaridad
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from catalogos.modelos.modelos import kCodigoPostal, kTipoAsentamiento, kMunicipio, kEntidad, kTipoProceso, kCentroCostos, kNivelEscolar, kFormacionEducativa

@gestion_empleados.route('/rh/gestion-empleados/generar-contratos', methods = ['POST', 'GET'])
def generar_contratoshonorarios():
    Entidad = db.session.query(kEntidad).filter_by(Activo=1).order_by(kEntidad.Entidad).all()    
    Municipio = db.session.query(kMunicipio).filter_by(idEntidad = 9, Activo=1).order_by(kMunicipio.Municipio).all()
    
    return render_template('/generar_contratohonorarios.html', title = 'Generar Contrato de Honorarios',
                           Entidad = Entidad,
                           Municipio = Municipio)

@gestion_empleados.route("/rh/gestion-empleados/generar-contratos-masivo", methods = ["POST", "GET"])
def generar_contrato_masivo():
    datos = request.get_json()

    if "ListaEmpleados" in datos:
        ListaEmpleados = datos["ListaEmpleados"]
        ListaNumeroContrato = datos["ListaNumeroContrato"]
        print(ListaEmpleados)
        print(ListaNumeroContrato)

        for idPersona, NumeroContrato in zip(ListaEmpleados, ListaNumeroContrato):
            respuesta = generar_contrato(idPersona=idPersona, NumeroContrato=NumeroContrato)

    return jsonify({"respuesta": respuesta})

@gestion_empleados.route("/rh/gestion-empleados/generar-contratos-masivo/busqueda-empleados", methods = ["GET", "POST"])
def busqueda_empleados():
    Busqueda = request.form.get("Busqueda")
    FechaInicio = request.form.get("FechaInicio")
    FechaFin = request.form.get("FechaFin")
    respuesta = 0

    resultados_sia = None
    resultados_centro_costos = None

    subquery = db.session.query(
        rEmpleadoPuesto.idPersona.label('id_persona'),
        func.max(rEmpleadoPuesto.FechaInicio).label('max_fecha_inicio')
    ).group_by(rEmpleadoPuesto.idPersona).subquery()

    # resultados_sia = db.session.query(rEmpleadoPuesto) \
    #     .join(rEmpleado, rEmpleadoPuesto.idPersona == rEmpleado.idPersona) \
    #     .join(tPersona, tPersona.idPersona == rEmpleado.idPersona) \
    #     .join(subquery, and_(
    #         subquery.c.idPersona == rEmpleadoPuesto.idPersona,
    #         subquery.c.max_fecha_inicio == rEmpleadoPuesto.FechaInicio  # .join("catalogos.kcentrocostos", rEmpleadoPuesto.idCentroCosto == "kcentrocostos".idCentroCosto) \
    #     )) \
    #     .filter(
    #         and_(
    #             rEmpleado.idTipoEmpleado == 1,
    #             or_(
    #                 tPersona.Nombre.contains(Busqueda),
    #                 tPersona.ApPaterno.contains(Busqueda),
    #                 tPersona.ApMaterno.contains(Busqueda),
    #                 rEmpleado.NumeroEmpleado.contains(Busqueda),
    #                 #kCentroCostos.CentroCosto.contains(Busqueda)
    #             )
    #         )
    #     ).order_by(tPersona.Nombre).all()
    
    # if len(resultados_sia) == 0:
    #     resultados_centro_costos = db.session.query(kCentroCostos) \
    #         .filter(
    #             #kCentroCostos.idCentroCosto.in_(centro_costos_ids),
    #         kCentroCostos.CentroCosto.contains(Busqueda)
    #         ).all()

    #     resultados_sia = []
    #     for centro_costo in resultados_centro_costos:
    #         resultados_sia.extend(
    #         db.session.query(rEmpleadoPuesto)
    #             .join(subquery,
    #                 (rEmpleadoPuesto.idPersona == subquery.c.idPersona) &
    #                 (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio))
    #             .join(rEmpleado)
    #             .join(tPersona)
    #             .filter(rEmpleadoPuesto.idCentroCosto == centro_costo.idCentroCosto, rEmpleado.idTipoEmpleado == 1)
    #             .order_by(tPersona.Nombre).all())

    # lista_empleados = []
    # empleado_data = {}

    # print(resultados_sia)
    # print(resultados_centro_costos)

    # for Empleado in resultados_sia:
    #     if Empleado.Empleado.Persona:
    #         empleado_data["Nombre"] = Empleado.Empleado.Persona.Nombre + ' ' + Empleado.Empleado.Persona.ApPaterno + ' ' + Empleado.Empleado.Persona.ApMaterno

    #     empleado_data["NumEmpleado"] = Empleado.Empleado.NumeroEmpleado
    #     empleado_data["idPersona"] = Empleado.idPersona

    #     centro_costo = db.session.query(kCentroCostos).filter_by(idCentroCosto = Empleado.idCentroCosto).first()
    #     empleado_data["CentroCostos"] = centro_costo.Clave

    #     lista_empleados.append(empleado_data.copy())

    # print(lista_empleados)

    ContratosExistentes = (db.session.query(rEmpleadoContrato, rEmpleadoPuesto)
        .join(subquery,
            subquery.c.id_persona == rEmpleadoContrato.idPersona  # Relación entre subconsulta y contrato
        )
        .join(rEmpleadoPuesto,
            (rEmpleadoPuesto.idPersona == subquery.c.id_persona) &
            (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio)
        )
        .join(rEmpleado, rEmpleado.idPersona == rEmpleadoContrato.idPersona)
        .join(tPersona, tPersona.idPersona == rEmpleado.idPersona)
        #.order_by(tPersona.Nombre, rEmpleadoContrato.FechaInicio)
    )

    if Busqueda != "":
        ContratosExistentes = ContratosExistentes.filter(
            and_(
                rEmpleado.idTipoEmpleado == 1,
                rEmpleado.Activo == 1,
                or_(
                    tPersona.Nombre.contains(Busqueda),
                    tPersona.ApPaterno.contains(Busqueda),
                    tPersona.ApMaterno.contains(Busqueda),
                    rEmpleado.NumeroEmpleado.contains(Busqueda)
                )
            )
        )
    
    if FechaInicio != "":
        FechaInicio = datetime.strptime(FechaInicio, '%d/%m/%Y')
        ContratosExistentes = ContratosExistentes.filter(rEmpleadoContrato.FechaInicio >= FechaInicio)

    if FechaFin != "":
        FechaFin = datetime.strptime(FechaFin, '%d/%m/%Y')
        ContratosExistentes = ContratosExistentes.filter(rEmpleadoContrato.FechaFin <= FechaFin)

    ContratosExistentes = ContratosExistentes.order_by(tPersona.ApPaterno, rEmpleadoContrato.FechaInicio).all()
    
    if len(ContratosExistentes) == 0:
        resultados_centro_costos = (
            db.session.query(kCentroCostos)
            .filter(
                or_(
                    kCentroCostos.CentroCosto.contains(Busqueda),
                    kCentroCostos.Clave.contains(Busqueda)
                )
            ).all()
        )

        ContratosExistentes = []

        for centro_costo in resultados_centro_costos:
            query = (
                db.session.query(rEmpleadoContrato, rEmpleadoPuesto)
                .join(subquery,
                    subquery.c.id_persona == rEmpleadoContrato.idPersona  # Relación entre subconsulta y contrato
                )
                .join(rEmpleadoPuesto,
                    (rEmpleadoPuesto.idPersona == subquery.c.id_persona) &
                    (rEmpleadoPuesto.FechaInicio == subquery.c.max_fecha_inicio)
                )
                .join(rEmpleado, rEmpleado.idPersona == rEmpleadoContrato.idPersona)
                .join(tPersona, tPersona.idPersona == rEmpleado.idPersona)
                .filter(rEmpleadoPuesto.idCentroCosto == centro_costo.idCentroCosto, rEmpleado.idTipoEmpleado == 1, rEmpleado.Activo == 1)
                #.order_by(tPersona.ApPaterno)
                #.all()
            )

            if FechaInicio != "":
                #FechaInicio = datetime.strptime(FechaInicio, '%d/%m/%Y')
                query = query.filter(rEmpleadoContrato.FechaInicio >= FechaInicio)

            if FechaFin != "":
                #FechaFin = datetime.strptime(FechaFin, '%d/%m/%Y')
                query = query.filter(rEmpleadoContrato.FechaFin <= FechaFin)

            ContratosExistentes.extend(query.order_by(tPersona.ApPaterno, rEmpleadoContrato.FechaInicio).all())

    lista_empleados = []
    empleado_data = {}

    for EmpleadoContrato, Empleado in ContratosExistentes:
        if Empleado.Empleado.Persona:
            empleado_data["Nombre"] = Empleado.Empleado.Persona.ApPaterno + ' ' + Empleado.Empleado.Persona.ApMaterno + ' ' + Empleado.Empleado.Persona.Nombre

            empleado_data["NumEmpleado"] = Empleado.Empleado.NumeroEmpleado
            empleado_data["idPersona"] = Empleado.idPersona

            centro_costo = db.session.query(kCentroCostos).filter_by(idCentroCosto = Empleado.idCentroCosto).first()
            empleado_data["CentroCosto"] = centro_costo.Clave

            empleado_data["FechaInicio"] = EmpleadoContrato.FechaInicio
            empleado_data["FechaFin"] = EmpleadoContrato.FechaFin

            empleado_data["ContratoGenerado"] = EmpleadoContrato.ContratoGenerado
            empleado_data["NumeroContrato"] = EmpleadoContrato.NumeroContrato

            empleado_data["url_descarga"] = url_for('gestion_empleados.descargar_contrato', nombre_archivo="Contrato " + empleado_data["Nombre"] + "_" + str(empleado_data["NumeroContrato"]) + ".pdf")

            lista_empleados.append(empleado_data.copy())

    if len(ContratosExistentes) == 0:
        respuesta = 1
    else:
        respuesta = 99
    
    print(lista_empleados)

    return jsonify({"respuesta": respuesta, "lista_empleados": lista_empleados})

#Generar Contratos de Honorarios
@gestion_empleados.route("/RH/generarContrato", methods = ['POST'])
def generar_contrato(idPersona, NumeroContrato):
    respuesta = 0
    if idPersona is None:
        idPersona = request.form.get("idPersona")

    EmpleadoPuesto = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona).first()
    PuestoHonorarios = db.session.query(tPuestoHonorarios).filter_by(idPuestoHonorarios = EmpleadoPuesto.idPuesto).first()
    EmpleadoContrato = db.session.query(rEmpleadoContrato).filter_by(idPersona = idPersona, NumeroContrato = NumeroContrato).first()
    empleado = db.session.query(tPersona).filter_by(idPersona = idPersona).first()
    PersonaEscolaridad = db.session.query(rPersonaEscolaridad).filter_by(idPersona = idPersona).first()
    print(PersonaEscolaridad)
    NivelEscolar = db.session.query(kNivelEscolar).filter_by(idNivel = PersonaEscolaridad.idNivelEscolaridad).first()
    FormacionEducativa = db.session.query(kFormacionEducativa).filter_by(idFormacionEducativa = PersonaEscolaridad.idFormacionEducativa).first()
    Domicilio = db.session.query(rDomicilio).filter_by(idPersona = idPersona, idTipoDomicilio = 1).first()
    Asentamiento = db.session.query(kCodigoPostal).filter(kCodigoPostal.CodigoPostal == Domicilio.idCP).order_by(kCodigoPostal.Consecutivo.desc()).first()
    TipoAsentamiento = db.session.query(kTipoAsentamiento).filter_by(idTipoAsentamiento = Domicilio.idTipoAsentamiento).first()
    Entidad = db.session.query(kEntidad).filter(kEntidad.idEntidad == Domicilio.idEntidad).order_by(kEntidad.Consecutivo.desc()).first()
    Municipio = db.session.query(kMunicipio).filter(kMunicipio.idMunicipio == Domicilio.idMunicipio, kMunicipio.idEntidad == Domicilio.idEntidad).order_by(kMunicipio.Consecutivo.desc()).first()
    hoy = datetime.now()

    meses = {
    "1":'ENERO',
    "2":'FEBRERO',
    "3":'MARZO',
    "4":'ABRIL',
    "5":'MAYO',
    "6":'JUNIO',
    "7":'JULIO',
    "8":'AGOSTO',
    "9":'SEPTIEMBRE',
    "10":'OCTUBRE',
    "11":'NOVIEMBRE',
    "12":'DICIEMBRE'
}

    nombre = empleado.ApPaterno + " " + empleado.ApMaterno + " " + empleado.Nombre
    dom = Domicilio.Vialidad + " NO. " + str(Domicilio.NumExterior) + ", "+ str(TipoAsentamiento.TipoAsentamiento).upper().rstrip() + " " + Asentamiento.Asentamiento + ", " + "C.P. "+ str(Domicilio.idCP)+ ", " + Municipio.Municipio.rstrip() + ", " + Entidad.Entidad
    if PuestoHonorarios.Nivel == "O33":
        AniosExperiencia = "2"
    else:
        AniosExperiencia = "4"
    #Abrir documento .docx
    template = DocxTemplate("rh/gestion_empleados/archivos/prueba.docx")
    #Diccionario con la información
    data_contrato = {
        'Nombre': nombre,
        'dia': str(hoy.day),
        'mes': meses[str(hoy.month)],
        'anio': str(hoy.year),
        'RFC': empleado.RFC,
        'NivelEscolar': NivelEscolar.NivelEscolar if NivelEscolar else "",
        'FormacionEducativa': FormacionEducativa.FormacionEducativa if FormacionEducativa else "",
        'Domicilio': dom,
        'AniosExperiencia': AniosExperiencia,
        'ImporteBruto': f"{EmpleadoContrato.ImporteBruto:,.2f}",
        'ImporteBrutoLetra': (num2words(EmpleadoContrato.ImporteBruto, lang='es')).upper() + " PESOS 00/100 M.N.",
        'Exhibiciones': (num2words(EmpleadoContrato.NumeroExhibicion, lang='es')).upper(),
        'MontoPactado': f"{EmpleadoContrato.MontoPactado:,.2f}",
        'DiaInicio': EmpleadoContrato.FechaInicio.day,
        'MesInicio': meses[str(EmpleadoContrato.FechaInicio.month)],
        'AnioInicio': EmpleadoContrato.FechaInicio.year,
        'DiaFin': EmpleadoContrato.FechaFin.day,
        'MesFin': meses[str(EmpleadoContrato.FechaFin.month)],
        'AnioFin': EmpleadoContrato.FechaFin.year
    }

    print(data_contrato)

    # Escribir información en el archivo .docx
    template.render(data_contrato)

    # 
    dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "contratos")
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Directorio %s creado" % dir)
    else:
        print("Directorio %s ya existe" % dir)

    # Guardar documento generado
    template.save(f"rh/gestion_empleados/archivos/contratos/Contrato " + nombre + "_" + NumeroContrato + ".docx")

    # Convertir archivo .docx a archivo .pdf
    pythoncom.CoInitialize()
    convert("rh/gestion_empleados/archivos/contratos/Contrato " + nombre + "_" + NumeroContrato + ".docx", "rh/gestion_empleados/archivos/contratos/Contrato " + nombre + "_" + NumeroContrato + ".pdf")

    if(os.path.exists(os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "contratos", ("Contrato " + nombre + "_" + NumeroContrato + ".pdf")))):
        EmpleadoContrato.ContratoGenerado = 1
        db.session.commit()
        respuesta = 99

    return respuesta

@gestion_empleados.route('/RH/descargar_contrato/<nombre_archivo>')
def descargar_contrato(nombre_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "contratos")

    return send_from_directory(directorio_archivos, nombre_archivo, as_attachment=True)