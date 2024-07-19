from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
from PyPDF2 import PdfMerger
import os
from dateutil.relativedelta import relativedelta

from .gestion_empleados import gestion_empleados
from rh.gestion_empleados.modelos.empleado import *
from rh.gestion_empleados.modelos.domicilio import *
from prestaciones.modelos.modelos import rEmpleadoConcepto
from general.modelos.modelos import tBitacora
#from catalogos.modelos.modelos import *
from app import db
from general.herramientas.funciones import *

@gestion_empleados.route('/rh/gestion-empleados/busqueda-empleado', methods = ['POST', 'GET'])
def busqueda_empleado():
    session["idPersona"] = None
    return render_template('/buscarempleado.html', title='Búsqueda de empleado',
                           current_user=current_user)

@gestion_empleados.route('/rh/gestion-empleados/agregar-empleado', methods = ['POST', 'GET'])
@gestion_empleados.route('/rh/gestion-empleados/modificar-empleado', methods = ['POST', 'GET'])
def modificar_empleado():
    if request.path == '/rh/gestion-empleados/modificar-empleado':
            idSelec = session.get("idPersona",None)
            if idSelec is None:
                return redirect('/rh/gestion-empleados/agregar-empleado')
            titulo = "Modifica empleado"
    else:
            #if current_user.idRol == 2 :
            #    return redirect('/rh/gestion-empleados/busqueda-empleado')
            idSelec = None
            session["idPersona"] = None
            titulo = "Agrega empleado"
    empleado  = db.session.query(tPersona).filter_by(idPersona = idSelec).first()

    # Catalogos para el empleado
    TipoPersona_datos = db.session.query(kTipoPersona).filter_by(Activo = 1,idTipoPersona = 1).order_by(kTipoPersona.idTipoPersona).all()
    EstCiv_datos = db.session.query(kEstadoCivil).filter_by(Activo = 1).order_by(kEstadoCivil.idEstadoCivil).all()
    Nacionalidad_datos = db.session.query(kNacionalidad).filter_by(Activo = 1).order_by(kNacionalidad.idNacionalidad).all()
    TipoEmpleado_datos = db.session.query(kTipoEmpleado).filter_by(Activo = 1).order_by(kTipoEmpleado.idTipoEmpleado).all()
    CentroCostos_datos = db.session.query(kCentroCostos).order_by(kCentroCostos.idCentroCosto).all()
    Quincena_datos = db.session.query(kQuincena).order_by(kQuincena.idQuincena).all()
    Escolaridad_datos = db.session.query(kEscolaridad).filter_by(Activo = 1).order_by(kEscolaridad.idEscolaridad).all()
    InstitucionEscolar = db.session.query(kInstitucionEscolar).filter_by(Activo = 1).order_by(kInstitucionEscolar.InstitucionEscolar).all()
    NivelEscolar = db.session.query(kNivelEscolar).filter_by(Activo = 1).order_by(kNivelEscolar.idNivel).all()
    FormacionEducativa = db.session.query(kFormacionEducativa).filter_by(Activo = 1).order_by(kFormacionEducativa.FormacionEducativa).all()
    Discapacidades = db.session.query(kDiscapacidad).filter_by(Activo = 1).order_by(kDiscapacidad.Discapacidad).all()
    Idiomas = db.session.query(kIdiomas).filter_by(Activo = 1).order_by(kIdiomas.Idioma).all()
    LenguasIndigenas = db.session.query(kLenguasIndigenas).filter_by(Activo = 1).order_by(kLenguasIndigenas.LenguaIndigena).all()

    # Catalogos para el domicilio
    Entidad_datos = db.session.query(kEntidad).filter_by(Activo = 1).order_by(kEntidad.idEntidad).all()
    TipoAsentamiento_datos = db.session.query(kTipoAsentamiento).filter_by(Activo = 1).order_by(kTipoAsentamiento.idTipoAsentamiento).all()
    Vialidad_datos = db.session.query(kVialidad).filter_by(Activo = 1).order_by(kVialidad.idVialidad).all()

    return render_template('/mas_informacion.html', title = titulo,
                           current_user = current_user,
                           TipoPersona = TipoPersona_datos,
                           EstCiv = EstCiv_datos,
                           Nacionalidad = Nacionalidad_datos,
                           TipoEmpleado = TipoEmpleado_datos,
                           CentroCostos = CentroCostos_datos,
                           Quincena = Quincena_datos,
                           Escolaridad = Escolaridad_datos,
                           NivelEscolar = NivelEscolar,
                           InstitucionEscolar = InstitucionEscolar,
                           FormacionEducativa = FormacionEducativa,
                           Entidad = Entidad_datos,
                           TipoAsentamiento = TipoAsentamiento_datos,
                           Vialidad = Vialidad_datos,
                           empleado = empleado,
                           Discapacidades = Discapacidades,
                           Idiomas = Idiomas,
                           LenguasIndigenas = LenguasIndigenas)

@gestion_empleados.route('/rh/gestion-empleados/guarda-empleado', methods = ['POST'])
def guardar_empleado():
    mapeo_nombres_persona = { #NombreEnFormulario : nombreEnBase
        'CURP': 'CURP',
        'Nombre': 'Nombre',
        'Paterno': 'ApPaterno',
        'Materno': 'ApMaterno',
        'Sexo': 'Sexo',
        'FechaNacimiento_format': 'FechaNacimiento',
        'RFC': 'RFC',
        'idEstadoCivil': 'idEstadoCivil',
        'idNacionalidad': 'idNacionalidad',
        'CalidadMigratoria': 'CalidadMigratoria',
        'TelCasa': 'TelCasa',
        'TelCelular': 'TelCelular',
        'idTipoPersona': 'idTipoPersona',
        'CorreoPersonal': 'CorreoPersonal',
        #'CorreoInstitucional': 'CorreoInstitucional',
        #'idTipoEmpleo': 'idTipoEmpleo',
        #'idTipoAlta': 'idTipoAlta',
        #'idGrupo': 'idGrupo',
        #'idPuesto': 'idPuesto',
        #'idPuestoJefe': 'idPuestoJefe',
        #'idCentroCosto': 'idCentroCosto',
        #'HoraEntrada': 'HoraEntrada',
        #'HoraSalida': 'HoraSalida',
        #'FecIngresoGob_format': 'FecIngresoGob',
        #'FecIngreso_format': 'FecIngreso',
        #'MesesServicio': 'MesesServicio',
        #'idEscolaridad': 'idEscolaridad',
        #'idNivelEscolaridad': 'idNivelEscolaridad',
        #'idInstitucionEscolar': 'idInstitucionEscolar',
        #'idFormacionEducativa': 'idFormacionEducativa',
        #'Especialidad': 'Especialidad',
        #'NumQuincena': 'NumQuincena',
        #'Clabe': 'Clabe',
        #'Banco': 'Banco',
        #'idEstatus': 'Activo',
    }

    mapeo_nombres_empleado = { #NombreEnFormulario : nombreEnBase
        'idTipoEmpleo': 'idTipoEmpleado',
        'idTipoAlta': 'idTipoAlta',
        'idGrupo': 'idGrupo',
        'HoraEntrada': 'HoraEntrada',
        'HoraSalida': 'HoraSalida',
        'FecIngresoGob_format' : 'FecIngGobierno',
        'FecIngreso_format': 'FecIngFonaes',
        'NumQuincena': 'idQuincena',
        'CorreoInstitucional': 'CorreoInstitucional'
    }

    mapeo_nombres_empleado_puesto = { #NombreEnFormulario : nombreEnBase
        'idPlazaHom' : 'idPuesto'
    }

    mapeo_nombres_escolaridad = { #NombreEnFormulario : nombreEnBase
        'idEscolaridad': 'idEscolaridad',
        'idNivelEscolaridad': 'idNivelEscolaridad',
        'idInstitucionEscolar': 'idInstitucionEscolar',
        'idFormacionEducativa': 'idFormacionEducativa',
        'Especialidad': 'Especialidad',
    }

    persona_data = {mapeo_nombres_persona[key]: request.form.get(key) for key in mapeo_nombres_persona.keys()}
    empleado_data = {mapeo_nombres_empleado[key]: request.form.get(key) for key in mapeo_nombres_empleado.keys()}
    empleado_puesto_data = {mapeo_nombres_empleado_puesto[key]: request.form.get(key) for key in mapeo_nombres_empleado_puesto.keys()}
    escolaridad_data = {mapeo_nombres_escolaridad[key]: request.form.get(key) for key in mapeo_nombres_escolaridad.keys()}

    idPersona = session.get("idPersona", None)
    nueva_persona = None
    nuevo_empleado = None
    nuevo_empleado_puesto = None
    nueva_escolaridad = None
    correo_enviado = False
    respuesta = {}
    empleado_data['Activo'] = 1
    empleado_puesto_data['idEstatusEP'] = 1

    ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
    if ultimo_idBitacora is None:
        idBitacora = 1
    else:
        idBitacora = ultimo_idBitacora + 1

    TipoEmpleado = empleado_data["idTipoEmpleado"]
    Periodo = datetime.now().year

    try:
        persona_existente = db.session.query(tPersona).filter_by(idPersona = idPersona).one()
        empleado_existente = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
        escolaridad_existente = db.session.query(rPersonaEscolaridad).filter_by(idPersona = idPersona).first()
        empleado_puesto_existente = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona).first()
        existe = 1
        # Si llegamos aquí, significa que ya existe un empleado
        # Envía correo correspondiente
        if not(empleado_existente.Activo == int(empleado_data["Activo"])):
            if(int(empleado_data["Activo"]) == 1):
                envia_correo("informatica","Reactivar",empleado_existente)
                crea_solicitud("Reactivar",empleado_existente)
                correo_enviado = True
            
        print("Actualiza")
        persona_data["idPersona"] = idPersona
        persona_existente.update(**persona_data)
        empleado_existente.update(**empleado_data)
        escolaridad_existente.update(**escolaridad_data)
        if(not empleado_puesto_existente.idEstatusEP):
            empleado_puesto_data["idPersona"] = idPersona
            empleado_puesto_data['FechaInicio'] = datetime.now().date()
            empleado_puesto_data['FechaTermino'] = None
            empleado_puesto_data['idEstatusEP'] = 1
            empleado_puesto_data['idCausaBaja'] = None
            empleado_puesto_data['Observaciones'] = None
            empleado_puesto_data['FechaEfecto'] = None
            empleado_puesto_data['idQuincena'] = None
            empleado_puesto_data['ClavePresupuestaSIA'] = None
            empleado_puesto_data['CodigoPlazaSIA'] = None
            empleado_puesto_data['CodigoPuestoSIA'] = None
            empleado_puesto_data['RHNETSIA'] = None
            empleado_puesto_data['idNivel'] = None
            empleado_puesto_data['ConservaVacaciones'] = 1
            nuevo_empleado_puesto = rEmpleadoPuesto(**empleado_puesto_data)
            db.session.add(nuevo_empleado_puesto)
            db.session.commit()
            nuevo_empleado_puesto.Puesto.idEstatusPuesto = 1

        # Actualizar los atributos de 'empleado_existente' con los valores de 'empleado_data'
        #for attr, value in persona_data.items():
        #    if not attr.startswith('_') and hasattr(empleado_existente, attr):
        #        setattr(empleado_existente, attr, value)
        respuesta["NumeroEmpleado"] = None

        TipoMovimiento = 2
    

    except NoResultFound:
        # Obtener el último valor de idPersona de la tabla de empleados y sumarle 1
        ultimo_id = db.session.query(func.max(tPersona.idPersona)).scalar()
        existe = 0
        if ultimo_id is None:
            nuevo_id_persona = 1
        else:
            nuevo_id_persona = ultimo_id + 1
            
        ultimo_Numero_Empleado = db.session.query(func.max(rEmpleado.NumeroEmpleado)).scalar()
        if ultimo_Numero_Empleado is None:
            nuevo_Numero_Empleado = 1
        else:
            nuevo_Numero_Empleado = ultimo_Numero_Empleado + 1

        # Asignar el nuevo valor de idPersona y NumeroEmpleado
        persona_data['idPersona'] = nuevo_id_persona
        empleado_data['idPersona'] = nuevo_id_persona
        empleado_data['NumeroEmpleado'] = nuevo_Numero_Empleado
        empleado_puesto_data['idPersona'] = nuevo_id_persona

        empleado_data['NoISSSTE'] = None
        empleado_data['FecAltaISSSTE'] = None
        empleado_data['Activo'] = 1

        empleado_puesto_data['ClavePresupuestaSIA'] = None
        empleado_puesto_data['CodigoPlazaSIA'] = None
        empleado_puesto_data['CodigoPuestoSIA'] = None
        empleado_puesto_data['RHNETSIA'] = None
        empleado_puesto_data['idNivel'] = None
        empleado_puesto_data['FechaInicio'] = datetime.now().date()
        empleado_puesto_data['FechaTermino'] = None
        empleado_puesto_data['idEstatusEP'] = 1
        empleado_puesto_data['idCausaBaja'] = None
        empleado_puesto_data['Observaciones'] = None
        empleado_puesto_data['FechaEfecto'] = None
        empleado_puesto_data['idQuincena'] = None
        empleado_puesto_data['ClavePresupuestaSIA'] = None
        empleado_puesto_data['CodigoPlazaSIA'] = None
        empleado_puesto_data['CodigoPuestoSIA'] = None
        empleado_puesto_data['RHNETSIA'] = None
        empleado_puesto_data['idNivel'] = None
        empleado_puesto_data['ConservaVacaciones'] = 1

        escolaridad_data['idPersona'] = nuevo_id_persona
        escolaridad_data['Consecutivo'] = 1

        nueva_persona = tPersona(**persona_data)
        db.session.add(nueva_persona)
        nuevo_empleado = rEmpleado(**empleado_data)
        db.session.add(nuevo_empleado)
        nuevo_empleado_puesto = rEmpleadoPuesto(**empleado_puesto_data)
        db.session.add(nuevo_empleado_puesto)
        nueva_escolaridad = rPersonaEscolaridad(**escolaridad_data)
        db.session.add(nueva_escolaridad)
        respuesta["guardado"] = True
        respuesta["NumeroEmpleado"] = empleado_data['NumeroEmpleado']

        crea_solicitud("Alta", nuevo_empleado)
        TipoMovimiento = 1

    ultimo_id_movimiento = db.session.query(func.max(rMovimientoEmpleado.idMovimientoEmpleado)).filter_by(idTipoMovimiento = TipoMovimiento).scalar()
    if ultimo_id_movimiento is None:
        idMovimientoEmpleado = 1
    else:
        idMovimientoEmpleado = ultimo_id_movimiento + 1

    nuevo_movimiento = rMovimientoEmpleado(idMovimientoEmpleado=idMovimientoEmpleado,
                                           idTipoMovimiento=TipoMovimiento,
                                           idPersonaMod=idPersona,
                                           idTipoEmpleado=TipoEmpleado,
                                           idUsuario=current_user.idPersona,
                                           Periodo=Periodo)
    
    db.session.add(nuevo_movimiento)

    nueva_bitacora = tBitacora(idBitacora=idBitacora,
                               idTipoMovimiento=TipoMovimiento,
                               idUsuario=current_user.idPersona)
    
    db.session.add(nueva_bitacora)
    # Realizar cambios en la base de datos
    db.session.commit()

    if nuevo_empleado is not None:
        # recuperar ID del nuevo empleado y devolverlo en el json
        empleado_existente = db.session.query(tPersona).filter_by(CURP = persona_data['CURP']).one()  
        session['idPersona'] = empleado_existente.idPersona

    return jsonify(respuesta)

@gestion_empleados.route('/rh/gestion-empleados/buscar-empleado', methods = ['POST', 'GET'])
def buscar_empleado():
     
    parametro = request.form.get("WParametro")
    esModal = request.form.get("esModal")

    # Dividir el parámetro en partes
    parametros_separados = parametro.split()

    filtro_comun = or_(
        tPersona.CURP.contains(parametro),
        tPersona.Nombre.contains(parametro),
        tPersona.ApPaterno.contains(parametro),
        tPersona.ApMaterno.contains(parametro),
        rEmpleado.NumeroEmpleado.contains(parametro)
    )

    if esModal:
        filtro_comun = and_(filtro_comun, rEmpleado.Activo == 1, tPersona.idTipoPersona == 1)

    # Agregar la búsqueda por partes del nombre
    if len(parametros_separados)>1:
        condiciones_nombre = []
        for parte_nombre in parametros_separados:
            condiciones_nombre.append(
                or_(
                    tPersona.Nombre.contains(parte_nombre),
                    tPersona.ApPaterno.contains(parte_nombre),
                    tPersona.ApMaterno.contains(parte_nombre)
                )
            )
        filtro_comun = and_(*condiciones_nombre)

    empleados = db.session.query(tPersona).join(rEmpleado).filter(filtro_comun).all()
    lista_empleados = []
    for empleado in empleados:
        if empleado is not None:
            NumeroEmpleado = empleado.Empleado.NumeroEmpleado
            empleado_dict = empleado.__dict__
            empleado_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            empleado_dict["NumeroEmpleado"] = NumeroEmpleado
            empleado_dict.pop("Empleado")
            lista_empleados.append(empleado_dict)
    return jsonify(lista_empleados)

@gestion_empleados.route('/rh/gestion-empleados/guardar-direccion', methods = ['POST'])
def guardar_direccion():
    idPersona = session.get('idPersona', None)
    if(idPersona is None):
        return jsonify({"guardado": False})
    else:
        insp = inspect(rDomicilio).all_orm_descriptors.keys()
        atributos_form = ['idPersona', 'idTipoDomicilio', 'CP', 'Entidad', 'Municipio', 'Localidad', 'TipoAsentamiento', 'Asentamiento',
                        'TipoVialidad', 'Vialidad', 'NumExt', 'NumInt', 'SN', 'DC', 'TipoVialidad01',
                        'Vialidad01', 'TipoVialidad02', 'Vialidad02', 'TipoVialidad03', 'Vialidad03']
        
        direccion = {}

        for column, key in zip(insp, atributos_form):
            if key in ["SN", "DC"]:
                direccion[column] = 0 if request.form.get(key) == None else 1
            else:
                direccion[column] = request.form.get(key)
        direccion['idPersona'] = idPersona
        direccion['Descripcion'] = None
        direccion['idDomicilio'] = idPersona

        try:
            direcciones_existentes = db.session.query(rDomicilio).filter_by(idPersona = idPersona).all()
            direccion_encontrada = None
            for direccion_existente in direcciones_existentes:
                if direccion_existente.idTipoDomicilio == int(direccion['idTipoDomicilio']):
                    direccion_encontrada = direccion_existente

            if direccion_encontrada is None:
                # Si no se encontró ninguna dirección que coincida, crea una nueva
                nueva_direccion = rDomicilio(**direccion)
                db.session.add(nueva_direccion)
            else:
                direccion_encontrada.update(**direccion)

        except NoResultFound:
            nueva_direccion = rDomicilio(**direccion)
            db.session.add(nueva_direccion)

        db.session.commit()

        return jsonify({"guardado": True})
    
@gestion_empleados.route('/rh/gestion-empleados/guardar-datos-bancarios', methods = ["POST"])
def guardar_datos_bancarios():
    idPersona = session.get('idPersona', None)
    if(idPersona is None):
        return jsonify({"guardado": False})
    else:
        #insp = inspect(rBancoPersona).all_orm_descriptors.keys()
        mapeo_nombres_datos_bancarios = {
            'idPersona': 'idPersona',
            'Clabe': 'Clabe',
            'idBanco': 'idBanco'}
        
        datos_bancarios = {mapeo_nombres_datos_bancarios[key]: request.form.get(key) for key in mapeo_nombres_datos_bancarios.keys()}
        
        nuevo_datos_bancarios = None

        Edo_Cuenta = request.files.get('EdoCuenta')
        

        datos_bancarios_existente = db.session.query(rBancoPersona).filter_by(idPersona = idPersona, Activo = 1).first()
        if(datos_bancarios_existente is None):
            datos_bancarios["idPersona"] = idPersona
            datos_bancarios["NumeroCuenta"] = datos_bancarios["Clabe"][6:17]
            datos_bancarios["Activo"] = 1
            datos_bancarios["Verificado"] = 0
            nuevo_datos_bancarios = rBancoPersona(**datos_bancarios)
            db.session.add(nuevo_datos_bancarios)
            #db.session.commit()
        
        else:
            if not datos_bancarios_existente.Verificado:
                datos_bancarios_existente.idBanco = datos_bancarios["idBanco"]
                datos_bancarios_existente.Clabe = datos_bancarios["Clabe"]
                datos_bancarios_existente.NumeroCuenta = datos_bancarios["Clabe"][6:17]
        
        db.session.commit()

        EXTENCIONES_PERMITIDAS = {'pdf'}
        if(Edo_Cuenta and archivo_permitido(Edo_Cuenta.filename, EXTENCIONES_PERMITIDAS)):
            if(datos_bancarios["Clabe"] != ""):
                filename = secure_filename(datos_bancarios["Clabe"] + '_' + str(idPersona) + '.pdf')
                dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "estados_cuenta")
                if not os.path.exists(dir):
                    os.mkdir(dir)
                    print("Directorio %s creado" % dir)
                else:
                    print("Directorio %s ya existe" % dir)

                dir = os.path.join(current_app.root_path, "rh", "gestion_empleados", "archivos", "estados_cuenta", filename)
                Edo_Cuenta.save(dir)

        return jsonify({"guardado": True})

@gestion_empleados.route('/rh/gestion-empleados/agregar-conceptos', methods = ["POST"])
def guardar_conceptos():
    idPersona = session.get('idPersona', None)
    if(idPersona is None):
        return jsonify({"guardado": False})
    else:
        Empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
        FechaIngGob = Empleado.FecIngGobierno
        FechaIngGob = datetime.combine(FechaIngGob, time())
        FechaActual = datetime.today()

        print(FechaIngGob, FechaActual)

        anios = relativedelta(FechaActual, FechaIngGob).years

        lista_idconceptos = ['7', 'CG', '38', '77D', '42A', '42B', '140', '199', '102', '1']
        lista_idtipo = ['P', 'P', 'P', 'D', 'D', 'D', 'D', 'D', 'D', 'D']

        if anios >= 5 and anios < 10:
            lista_idconceptos.insert(1, 'A1')
            lista_idtipo.insert(1, 'P')
        if anios >=10 and anios < 15:
            lista_idconceptos.insert(1, 'A2')
            lista_idtipo.insert(1, 'P')
        if anios >=15 and anios < 20:
            lista_idconceptos.insert(1, 'A3')
            lista_idtipo.insert(1, 'P')
        if anios >=20 and anios < 25:
            lista_idconceptos.insert(1, 'A4')
            lista_idtipo.insert(1, 'P')
        if anios >=25:
            lista_idconceptos.insert(1, 'A5')
            lista_idtipo.insert(1, 'P')

        nuevo_concepto = None
        datos_conceptos = {}
        datos_conceptos["idPersona"] = idPersona
        for indice in range(0, len(lista_idconceptos)):
            concepto = db.session.query(kConcepto).filter_by(idTipoConcepto = lista_idtipo[indice], idConcepto = lista_idconceptos[indice]).first()
            if(concepto is not None):
                if db.session.query(rEmpleadoConcepto).filter_by(idPersona = idPersona, idTipoConcepto = concepto.idTipoConcepto, idConcepto = concepto.idConcepto).first() is None:
                    datos_conceptos["idTipoConcepto"] = concepto.idTipoConcepto
                    datos_conceptos["idConcepto"] = concepto.idConcepto
                    datos_conceptos["Porcentaje"] = concepto.Porcentaje
                    datos_conceptos["Monto"] = concepto.Monto
                    datos_conceptos["NumeroContrato"] = 1
                    datos_conceptos["FechaInicio"] = None
                    datos_conceptos["FechaFin"] = None
                    datos_conceptos["PagoUnico"] = 0
                    nuevo_concepto = rEmpleadoConcepto(**datos_conceptos)
                    db.session.add(nuevo_concepto)
        
        db.session.commit()

        return jsonify({"guardado": True})
    
@gestion_empleados.route("/rh/gestion-empleados/agregar-expediente", methods = ["POST"])
def agregar_documentos():
    # Obtener Nombre y Apellido del empleado
    idPersona = session.get("idPersona", None)
    Empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()
    NumEmpleado = Empleado.NumeroEmpleado
    Nombre = Empleado.Persona.Nombre
    ApPaterno = Empleado.Persona.ApPaterno
    ApMaterno = Empleado.Persona.ApMaterno

    # Obtener archivos
    ActaNacimiento = request.files.get("ActaNacimiento")
    Titulo = request.files.get("Titulo")
    CartillaMilitar = request.files.get("CartillaMilitar")
    ComprobanteDomicilio = request.files.get("ComprobanteDomicilio")
    IdentificacionOficial = request.files.get("IdentificacionOficial")
    ArchivoCURP = request.files.get("ArchivoCURP")
    ArchivoRFC = request.files.get("ArchivoRFC")
    
    # Inicializar resultados
    resultado = {}
    expediente_data = {}
    resultado["NoArchivo"] = True
    resultado["ExpedienteNombre"] = False
    expediente_data["idPersona"] = idPersona

    expediente_existente = db.session.query(rPersonaExpediente).filter_by(idPersona = idPersona).first()
    if expediente_existente is not None:
        expediente_data = expediente_existente.__dict__
        expediente_data = expediente_data.copy()
        expediente_data.pop("_sa_instance_state")
    else:
        expediente_data["ActaNacimiento"] = 0
        expediente_data["Titulo"] = 0
        expediente_data["CartillaMilitar"] = 0
        expediente_data["ComprobanteDomicilio"] = 0
        expediente_data["IdentificacionOficial"] = 0
        expediente_data["ArchivoCURP"] = 0
        expediente_data["ArchivoRFC"] = 0

    # Crear objeto para combinar PDF's
    merger = PdfMerger()

    if ActaNacimiento:
        merger.append(ActaNacimiento)
        expediente_data["ActaNacimiento"] = 1
        resultado["NoArchivo"] = False

    if Titulo:
        merger.append(Titulo)
        expediente_data["Titulo"] = 1
        resultado["NoArchivo"] = False

    if CartillaMilitar:
        merger.append(CartillaMilitar)
        expediente_data["CartillaMilitar"] = 1
        resultado["NoArchivo"] = False

    if ComprobanteDomicilio:
        merger.append(ComprobanteDomicilio)
        expediente_data["ComprobanteDomicilio"] = 1
        resultado["NoArchivo"] = False

    if IdentificacionOficial:
        merger.append(IdentificacionOficial)
        expediente_data["IdentificacionOficial"] = 1
        resultado["NoArchivo"] = False
    
    if ArchivoCURP:
        merger.append(ArchivoCURP)
        expediente_data["ArchivoCURP"] = 1
        resultado["NoArchivo"] = False

    if ArchivoRFC:
        merger.append(ArchivoRFC)
        expediente_data["ArchivoRFC"] = 1
        resultado["NoArchivo"] = False

    # Crear nombre del archivo
    NombreCompleto = Nombre + " " + ApPaterno + " " + ApMaterno
    filename = str(NumEmpleado) + "_" + NombreCompleto + ".pdf"

    if not resultado["NoArchivo"]:
        # Directorio para almacenar los expedientes
        dir = os.path.join("rh", "gestion_empleados", "archivos", "expedientes")

        # Si no existe el directorio
        if not os.path.exists(dir):
            # Se crea
            os.mkdir(dir)
            print("Directorio %s creado" % dir)
        else:
            print("Directorio %s ya existe" % dir)

        # Si existe un expediente con nombre por idPersona
        if os.path.exists(os.path.join("rh", "gestion_empleados", "archivos", "expedientes", filename)):
            # Se agrega para hacer la combinación
            merger.append(os.path.join("rh", "gestion_empleados", "archivos", "expedientes", filename))
            print("Existe con expediente")

        else:
            # Obtener lista de archivos en el directorio
            archivos = os.listdir(dir)
            # Recorrer la lista
            for archivo in archivos:
                if archivo.startswith("~$"):
                    # Eliminar copias temporales
                    archivos.remove(archivo)
                # Verificar si hay un archivo con Nombre o Apellido del empleado
                if NombreCompleto.lower() in archivo.lower():
                    resultado["ExpedienteNombre"] = True
                    # Si hay un archivo se sale del ciclo
                    break

            # Si hay un archivo con Nombre
            if resultado["ExpedienteNombre"]:
                dir = os.path.join("rh", "gestion_empleados", "archivos", "expedientes", archivo)
                # Se agrega a la combinación
                merger.append(dir)

        dir = os.path.join("rh", "gestion_empleados", "archivos", "expedientes", filename)
        merger.write(dir)

    if expediente_existente is not None:
        expediente_existente.update(**expediente_data)
    else:
        nuevo_expediente = rPersonaExpediente(**expediente_data)
        db.session.add(nuevo_expediente)
    
    db.session.commit()

    return jsonify(resultado)

@gestion_empleados.route("/rh/gestion-empleados/agregar-mas-informacion", methods = ["POST"])
def agregar_mas_informacion():
    mapeo_nombres_mas_informacion = { #NombreEnFormulario : nombreEnBase
        'Idioma1': 'idIdioma',
        'Indigena': 'idIdiomaIndigena',
        'Afroamericano': 'idAfroamericano',
        'Discapacidad': 'idDiscapacidad'
    }

    mas_informacion_data = {mapeo_nombres_mas_informacion[key]: request.form.get(key) for key in mapeo_nombres_mas_informacion.keys()}
    idPersona = session.get("idPersona", None)
    mas_informacion_data["idPersona"] = idPersona
    NumIdiomas = int(request.form.get("NumIdiomas"))
    NumIndigenas = int(request.form.get("NumIndigenas"))
    print(NumIdiomas, NumIndigenas)

    mas_informacion_existente = db.session.query(rPersonaMasInformacion).filter_by(idPersona = idPersona).first()
    if mas_informacion_existente is not None:
        mas_informacion_existente.update(**mas_informacion_data)

        if NumIdiomas > 0:
            for i in range(1, NumIdiomas + 1):
                idIdioma = request.form.get("Idioma" + str(i))
                if db.session.query(rPersonaIdioma).filter_by(idPersona = idPersona, idIdioma = idIdioma).first() is None:
                    nuevo_idioma = rPersonaIdioma(idPersona = idPersona, idIdioma = idIdioma)
                    print(nuevo_idioma)
                    db.session.add(nuevo_idioma)

        if mas_informacion_data["idIdiomaIndigena"] == 1 and NumIndigenas > 0:
            for i in range(1, NumIndigenas + 1):
                idIndigena = request.form.get("Indigena" + str(i))
                if db.session.query(rPersonaIndigena).filter_by(idPersona = idPersona, idIndigena = idIndigena).first is None:
                    nuevo_indigena = rPersonaIndigena(idPersona=idPersona, idIndigena=idIndigena)
                    db.session.add(nuevo_indigena)
    else:
        nuevo_mas_informacion = rPersonaMasInformacion(**mas_informacion_data)
        db.session.add(nuevo_mas_informacion)

    db.session.commit()

    return jsonify({"guardado": True})


@gestion_empleados.route('/rh/gestion-empleados/buscar-curp', methods = ['POST'])
def buscar_curp():
    curp = request.form.get("CURP")
    empleado = db.session.query(tPersona).filter_by(CURP=curp).first()
    if empleado is None:
        empleado = consultar_curp(curp)
        session["idPersona"] = None
        return jsonify(empleado)
    else:
        empleado_dict = empleado.__dict__
        empleado_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        session["idPersona"] = empleado_dict["idPersona"]

        return jsonify(empleado_dict)
    
@gestion_empleados.route('/rh/gestion-empleados/cargar-cp', methods = ['POST'])
def cargar_CP():
    Entidad  = request.form.get("Entidad")
    Municipio  = request.form.get("Municipio")
    TipoAsentamiento  = request.form.get("TipoAsentamiento")
    Asentamiento = request.form.get("Asentamiento")
    CPbusqueda = db.session.query(kCodigoPostal).filter_by(idEntidad = Entidad, idMunicipio = Municipio, idTipoAsentamiento = TipoAsentamiento, idAsentamiento = Asentamiento, Activo = 1).first()
    
    if CPbusqueda:
        codigo_postal = CPbusqueda.CodigoPostal
        return jsonify(codigo_postal)
    else:
        return "no encontrado"
    
@gestion_empleados.route('/rh/gestion-empleados/buscar-cp', methods = ['POST'])
def buscar_CP():
    CP = request.form.get("CP")
    CPbusqueda = db.session.query(kCodigoPostal).filter_by(CodigoPostal = CP, Activo = 1).first()
    if CPbusqueda:
        CPbusqueda = CPbusqueda.__dict__
        CPbusqueda.pop("_sa_instance_state", None)
        return jsonify(CPbusqueda)
    else:
        return "no encontrado"
    
@gestion_empleados.route('/rh/gestion-empleados/selecciona-empleado', methods = ['POST', 'GET'])
def seleccionar_empleado():
    idPersona = request.form.get("idPersona")
    session['idPersona'] = idPersona
    empleado = db.session.query(tPersona).filter_by(idPersona = idPersona).first()
    if empleado is not None:
        NumeroEmpleado = empleado.Empleado.NumeroEmpleado
        empleado = empleado.__dict__
        empleado.pop("_sa_instance_state", None)
        empleado["NumeroEmpleado"] = str(NumeroEmpleado)
        empleado.pop("Empleado")
    return jsonify(empleado)

@gestion_empleados.route('/rh/gestion-empleados/obtener-banco', methods = ['POST'])
@permisos_de_consulta
def obtener_Banco():
    subClabe = request.form.get("subClabe")
    try:
        Banco = db.session.query(kBancos).filter_by(Codigo = subClabe).one()
        Banco_dict = Banco.__dict__
        Banco_dict.pop("_sa_instance_state", None)
        return jsonify(Banco_dict)
    
    except NoResultFound:
        return jsonify({"Nombre": "Banco no encontrado"})