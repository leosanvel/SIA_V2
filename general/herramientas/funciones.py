from flask import redirect, url_for, request
from flask_login import current_user
from functools import wraps
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import requests.exceptions
from sqlalchemy import and_, or_, cast, String
from sqlalchemy.orm.exc import NoResultFound
from datetime import time, date, datetime, timedelta
from app import db

import smtplib
from email.message import EmailMessage

from catalogos.modelos.modelos import kQuincena,kConcepto
from rh.gestion_asistencias.modelos.modelos import tIncidencia, tJustificante, tChecador, rSancionPersona, tIncidenciasPasadas
from rh.gestion_empleados.modelos.empleado import rEmpleado, rEmpleadoPuesto
from informatica.modelos.modelos import rSolicitudEstado
from nomina.modelos.modelos import tNomina

from prestaciones.modelos.modelos import rEmpleadoConcepto
from rh.gestion_tiempo_no_laboral.modelos.modelos import rDiasPersona


def permisos_de_consulta(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.Activo == 1:
            return view_func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('autenticacion.inicio_sesion'))
        else:
            return "Usuario INACTIVO"
    return decorated_view

# Calcular edad con fecha de nacimiento
def calcular_edad(fec_nac):
    hoy = datetime.today()
    edad = hoy.year - fec_nac.year - ((hoy.month, hoy.day) < (fec_nac.month, fec_nac.day))
    return edad

# Consultar CURP
def consultar_curp(CURP):
    url = "https://sia.inaes.gob.mx/ServiciosWeb/ConsultaCurp?curp="
    # Unión de la URL con la CURP a consultar
    url = url + CURP

    try:
        # Obtención del HTML de respuesta a la consulta
        page = requests.get(url, verify=False, timeout = 2.5)

        # Si la respuesta es correcta
        if page.status_code == 200:
            html_content = page.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Se filtra la información
            Status = soup.find('td', id = 'estatusOperacion').text.strip()
            empleado = {}
            empleado["Mensaje"] = soup.find('td', id = 'mensage').text.strip()
            empleado["Status"] = Status
            empleado["CURP"] = CURP

            # Si es estatus es correcto
            if(Status == "EXITOSO"):
                # Se obtiene el estatus de la CURP
                Status_CURP = soup.find('td', id = 'statusCurp').text.strip()
                # Si la CURP es válida
                if(Status_CURP != "BSU"):
                    # Se obtiene el resto de la información
                    empleado["CURP"] = soup.find('td', id = 'CURP').text.strip()
                    empleado["Nombre"] = soup.find('td', id = 'nombres').text.strip()
                    empleado["ApPaterno"] = soup.find('td', id = 'apellido1').text.strip()
                    empleado["ApMaterno"] = soup.find('td', id = 'apellido2').text.strip()
                    empleado["Sexo"] = soup.find('td', id = 'sexo').text.strip()
                    empleado["FechaNacimiento"] = soup.find('td', id = 'fechNac').text.strip()
                    empleado["Edad"] = calcular_edad(datetime.strptime(empleado["FechaNacimiento"], "%d/%m/%Y"))
                    #empleado["Nacionalidad"] = soup.find('td', id = 'nacionalidad').text.strip()
                else:
                    empleado["Status"] = "BSU"
            # Se retorna un diccionario con la información
            return empleado
    except requests.exceptions.Timeout:
        print("Tiempo de respuesta vencido.")
        empleado = {"tiempo_error": True}
        return empleado
    except requests.exceptions.ConnectionError:
        print("Error de conexión.")
        empleado = {"conexion_error": True}
        return empleado
    except requests.exceptions.RequestException:
        print("Se produjo una ambigüedad.")
        empleado = {"error": True}
        return empleado

# Función para eliminar los caracteres "" de un string y poder visualizar en HTML
def eliminar_caracter(cad):
    indices = []
    c = "\""
    cad_aux = cad
    for pos, char in enumerate(cad):
        if char == c:
            indices.append(pos)
    
    if(indices):
        for i in indices:
            i = i - indices.index(i)
            cad_aux = cad_aux[:i] + cad_aux[i + 1:]
    

    return cad_aux

# Función para saber si la extensión es la permitida
def archivo_permitido(filename, EXTENCIONES_PERMITIDAS):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in EXTENCIONES_PERMITIDAS




def envia_correo(receptor, motivo, objeto):
    print("Función de correo ejecutada")
    return 0
    # Configura los detalles del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587  # Puerto del servidor SMTP
    sender_email = 'sanvel.eli@gmail.com'
    password = 'xdls ksdd ginv penp'

    # Configura los detalles del mensaje
    if receptor == "informatica":
        receiver_email = "leli.sanchezv@cinvestav.mx"
    elif receptor == "rh":
        receiver_email = "leli.sanchezv@cinvestav.mx"
    else:
        receiver_email = "leli.sanchezv@cinvestav.mx"

    if motivo == "Alta":
        subject = 'Alta de empleado'
        body = 'Se solicita que el empleado ' + objeto.Nombre +' '+ objeto.ApPaterno +' '+ objeto.ApMaterno + ' con número de empleado ' + str(objeto.NumeroEmpleado) + ', sea dado de ALTA en todos los sistemas y correo electrónico.'
    elif motivo == "Baja":
        subject = 'Baja de empleado'
        body = 'Se solicita que el empleado ' + objeto.Nombre +' '+ objeto.ApPaterno +' '+ objeto.ApMaterno + ' con número de empleado ' + str(objeto.NumeroEmpleado) + ', sea dado de BAJA de todos los sistemas y correo electrónico.'
    elif motivo == "Reactivar":
        subject = 'Reactivación de empleado'
        body = 'Se solicita que el empleado ' + objeto.Nombre +' '+ objeto.ApPaterno +' '+ objeto.ApMaterno + ' con número de empleado ' + str(objeto.NumeroEmpleado) + ', sea REACTIVADO en todos los sistemas y correo electrónico.'

    elif motivo == "solicitud_completada":
        subject = 'Solicitud completada'
        body = 'La solicitud con descripción:' + objeto.Descripcion +' ha sido completada.'


    # Construye el mensaje
    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.set_content(body)

    # Inicia una conexión con el servidor SMTP
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Inicia una conexión TLS
        server.login(sender_email, password)
        # Envía el correo electrónico
        server.send_message(message)

def procesar_nomina(nomina_data, VistaPrevia = None):
    respuesta={}
    respuesta["NoChecador"] = False
    respuesta["NoPersonas"] = False
    respuesta["NoCoincidencias"] = False
    respuesta["NoIncidencias"] = False
    respuesta["Existente"] = False
    respuesta["Creado"] = False

    lista_nomina = []

    quincena = db.session.query(kQuincena).filter(kQuincena.idQuincena == nomina_data["NumeroQuincena"]).one()
    nomina_data["PeriodoQuincena"] = quincena.FechaFin.year
    # Obtener las incidencias de checador
    incidencias = db.session.query(tIncidencia).filter(
        or_(
            and_(
                tIncidencia.FechaInicio >= quincena.FechaInicio,
                tIncidencia.FechaInicio <= quincena.FechaFin
            ),
            and_(
                tIncidencia.FechaFin >= quincena.FechaInicio,
                tIncidencia.FechaFin <= quincena.FechaFin
            )
        )
    ).all()

    # Iterar sobre las incidencias y actualizar Tchecador
    for incidencia in incidencias:
        actualizar_tchecador(incidencia)

    if not incidencias:
        respuesta["NoIncidencias"] = True

    # Obtener los justificantes de Tjustificante
    justificantes = db.session.query(tJustificante).filter(
        or_(
            and_(
                tJustificante.FechaInicio >= quincena.FechaInicio,
                tJustificante.FechaInicio <= quincena.FechaFin
            ),
            and_(
                tJustificante.FechaFin >= quincena.FechaInicio,
                tJustificante.FechaFin <= quincena.FechaFin
            )
        )
    ).all()

    # Iterar sobre los justificantes y actualizar Tchecador
    for justificante in justificantes:
        actualizar_tchecador(justificante)

    Personas = db.session.query(rEmpleado).filter_by(idTipoEmpleado = nomina_data["TipoEmpleado"], Activo = 1).all()
    contador = 1

    if not Personas:
        respuesta["NoPersonas"] = True
    Checadores = db.session.query(tChecador).filter(tChecador.Fecha <= quincena.FechaFin).filter(tChecador.Fecha >= quincena.FechaInicio).all()

    if not Checadores:
        respuesta["NoChecador"] = True
    try:
        nomina_existente = db.session.query(tNomina).filter_by(idQuincena=quincena.idQuincena, PeriodoQuincena=quincena.FechaFin.year).one()
        respuesta["Existente"] = True
    except NoResultFound:
        respuesta["Existente"] = False
    
    for Persona in Personas:
        if respuesta["Existente"]:
            Checadores = db.session.query(tChecador)\
                .filter(tChecador.idPersona == Persona.idPersona)\
                .filter(tChecador.Fecha <= quincena.FechaFin)\
                .filter(or_(tChecador.HoraEntrada == None, tChecador.HoraSalida == None))\
                .filter(tChecador.idQuincenaReportada == quincena.idQuincena)\
                .order_by(tChecador.Fecha)\
                .limit(3)\
                .all()

        else:
            # Filtrar que al Fecha sea menor la FechaFinal de la quincena, que tenga null en HoraEntrada u HoraSalida o ambas, y que tenga null en idQuincenaReportada
            # Checadores = db.session.query(Tchecador).filter_by(idPersona=Persona.idPersona, Fecha <= quincena.FechaFin).all()
            Checadores = db.session.query(tChecador)\
                .filter(tChecador.idPersona == Persona.idPersona)\
                .filter(tChecador.Fecha <= quincena.FechaFin)\
                .filter(or_(tChecador.HoraEntrada == None, tChecador.HoraSalida == None))\
                .filter(tChecador.idQuincenaReportada == None)\
                .order_by(tChecador.Fecha)\
                .limit(3)\
                .all()

        # Se agregará información a lista_nomina solo si hay días con HoraEntrada o HoraSalida como None
        if Checadores:
            respuesta["NoIncidencias"] = False
            nomina_data["N"] = contador
            nomina_data["idPersona"] = Persona.idPersona
            nomina_data["ADSCRIP"] = "000"
            nomina_data["Nivel"] = "X0"
            nomina_data["NombrePersona"] = Persona.Persona.ApPaterno + " " + Persona.Persona.ApMaterno + " " + Persona.Persona.Nombre
            nomina_data["RFC"] = Persona.Persona.RFC
            nomina_data["NumeroEmpleado"] = Persona.NumeroEmpleado
            nomina_data["DiasIncidencias"] = []
            # nomina_data["Estatus"] = 1
            # nomina_data["idRemitente"] = current_user.id

            for Checador in Checadores:
                fecha_formateada = Checador.Fecha
                nomina_data["DiasIncidencias"].append(fecha_formateada)
                if (VistaPrevia is None):
                    Checador.idQuincenaReportada = nomina_data["NumeroQuincena"]
            if (VistaPrevia is None):
                db.session.commit()

            nomina_data["NumeroDias"] = len(nomina_data["DiasIncidencias"])
            fechas_agrupadas = defaultdict(list)
            # Agrupamos las fechas por mes y año
            for fecha in nomina_data["DiasIncidencias"]:
                fechas_agrupadas[(fecha.month, fecha.year)].append(fecha)

            # Convertimos las fechas agrupadas en una lista de cadenas formateadas
            fechas_formateadas = []
            for mes, año in fechas_agrupadas:
                fechas_mes = fechas_agrupadas[(mes, año)]
                fechas_mes_str = [fecha.strftime("%d") for fecha in fechas_mes]
                fechas_formateadas.append(", ".join(fechas_mes_str) + "/" + str(mes).zfill(2) + "/" + str(año)[-2:])
            fechas = ", ".join(fechas_formateadas)
            nomina_data["DiasIncidencias"] = fechas

            lista_nomina.append(nomina_data.copy())
            
    if(not lista_nomina):
        respuesta["NoCoincidencias"] = True
    else:
        respuesta["Creado"] = True

    if respuesta["Existente"] or respuesta["Creado"]:
        respuesta["lista_nomina"] = lista_nomina
    
    return respuesta
    
def actualizar_tchecador(incidencia_o_justificante):
    id_persona = incidencia_o_justificante.idPersona
    fecha_inicio = incidencia_o_justificante.FechaInicio
    fecha_fin = incidencia_o_justificante.FechaFin

    # Obtener registros de Tchecador para la persona y el rango de fechas
    checadores = db.session.query(tChecador).filter(
        tChecador.idPersona == id_persona,
        tChecador.Fecha >= fecha_inicio,
        tChecador.Fecha <= fecha_fin
    ).all()

    # Iterar sobre los registros y actualizar según el tipo de incidencia o justificante
    for checador in checadores:
        if isinstance(incidencia_o_justificante, tIncidencia):
            tipo_incidencia = incidencia_o_justificante.idTipo
            checador.idIncidencia = incidencia_o_justificante.idIncidencia
            if tipo_incidencia == 1:
                checador.HoraEntrada = None
                checador.HoraSalida = None
            elif tipo_incidencia == 2:
                checador.HoraEntrada = None
            elif tipo_incidencia == 6:
                checador.HoraSalida = None


        elif isinstance(incidencia_o_justificante, tJustificante):
            tipo_justificante = incidencia_o_justificante.idTipo
            checador.idJustificante = incidencia_o_justificante.idJustificante
            if tipo_justificante == 2:  # Entrada
                checador.HoraEntrada = time(9, 0, 0)
            elif tipo_justificante == 6:  # Salida
                checador.HoraSalida = time(18, 0, 0)
            else:
                checador.HoraEntrada = time(9, 0, 0)
                checador.HoraSalida = time(18, 0, 0)
        else:
            checador.HoraEntrada = time(9, 0, 0)
            checador.HoraSalida = time(18, 0, 0)

    # Realizar cambios en la base de datos
    db.session.commit()

def serialize_datetime(obj): 
    if isinstance(obj, datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable")

def calcular_quincena(fecha):
    # hoy = datetime.now()
    mes = fecha.month
    quincena = mes*2
    if((fecha.day//16) == 0):
        quincena = quincena - 1

    return quincena

def crea_solicitud(motivo,empleado_existente):
    solicitud_data = {
        "idSolicitud" : None,
        "Solicitud" : motivo,
        "Descripcion" : motivo + " al empleado #" + str(empleado_existente.NumeroEmpleado) + " "+ empleado_existente.Persona.Nombre + " " + empleado_existente.Persona.ApPaterno + " " + empleado_existente.Persona.ApMaterno + ".",
        "idEstadoSolicitud" : 1,
    }
    
    
    nueva_solicitud = rSolicitudEstado(**solicitud_data)
    db.session.add(nueva_solicitud)
    # Realizar cambios en la base de datos
    db.session.commit()
    print("Solicitud agregada a la base de datos")

def ejecutar_tareas_diarias():
    revision_baja_empleados()
    verificar_antiguedad_prima_quinquenal()
    verificar_antiguedad_articulo_37_todos()
    elimina_vacaciones_vencidas()
    print("FUNCION AUTOMATICA EJEUTADA AL INICIAR EL DÍA:")
    hoy = datetime.today().date()
    print(hoy)


def revision_baja_empleados(idPersona = None):
    hoy = datetime.today().date()
    puestos_empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona,FechaEfecto=hoy, idEstatusEP = 1).all()
    print("Dando de baja a los siguientes puestos:")
    print(puestos_empleado)
    if puestos_empleado:
        for puesto in puestos_empleado:
            puesto.FechaTermino = hoy

            # cambiar en tPuesto idEstatusPuesto # (1 = Ocupada, 2 = Vacante)
            if puesto.Empleado.idTipoEmpleado == 2:
                puesto.Puesto.idEstatusPuesto = 2

            # Desactivar el puesto del empleado
            puesto.idEstatusEP = 0

            #asignar fecha termino
            puesto.FechaTermino = datetime.today()

            # desactivar empleado
            puesto.Empleado.Activo = 0

            # vaciar: rconcepto empleado
            elimina_conceptos_empleado = db.session.query(rEmpleadoConcepto).filter_by(idPersona = puesto.idPersona).delete()

            #Eliminar o conservar vacaciones
            if puesto.ConservaVacaciones != 1:
                print("vacaciones eliminadas")
                vacaciones_eliminadas = db.session.query(rDiasPersona).filter_by(idPersona = puesto.idPersona).delete()
            
            empleado_existente = db.session.query(rEmpleado).filter_by(idPersona = puesto.idPersona).first()
            crea_solicitud("Baja", empleado_existente)
        db.session.commit()
    else:
        print("Ningún empleado termina Hoy")

def verificar_antiguedad_prima_quinquenal():
    
    # Ejemplo de función para verificar la antigüedad de los empleados
    hoy = datetime.today().date()
    empleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idEstatusEP == 1).all()
    aniversario = False
    for puesto in empleadoPuesto:
        # Verificar que FecIngGobierno no sea None
        if puesto.Empleado.FecIngGobierno is not None:
            FecIngGobierno = puesto.Empleado.FecIngGobierno
        else:
            FecIngGobierno = puesto.Empleado.FecIngFonaes
            # print("Error: No se encontró la FecIngGobierno")
            continue

        # Verificar si hoy es el aniversario de ingreso al gobierno
        if (FecIngGobierno.month, FecIngGobierno.day) == (hoy.month, hoy.day):
            # Calcular la antigüedad en años completos
            antiguedad_en_anios = hoy.year - FecIngGobierno.year

            # Determinar el concepto correspondiente basado en los años de antigüedad
            if 5 <= antiguedad_en_anios < 10:
                concepto = "A1"
            elif 10 <= antiguedad_en_anios < 15:
                concepto = "A2"
            elif 15 <= antiguedad_en_anios < 20:
                concepto = "A3"
            elif 20 <= antiguedad_en_anios < 25:
                concepto = "A4"
            elif antiguedad_en_anios >= 25:
                concepto = "A5"
            else:
                concepto = "Ninguno"  # Si la antigüedad es menor a 5 años

            asignar_concepto_quinquenio(puesto.idPersona, concepto)
            print(f"Empleado ID: {puesto.Empleado.NumeroEmpleado}, Antigüedad en gobierno: {antiguedad_en_anios} años, Concepto asignado: {concepto}")
            aniversario = True
    if not aniversario:
        print("Ningún empleado cumple años hoy")

def asignar_concepto_quinquenio(idPersona, idConcepto):
    if idConcepto == "Ninguno":
        return 0
    # Lista de conceptos de A1 a A5
    conceptos_a_eliminar = ["A1", "A2", "A3", "A4", "A5"]

    elimina_concepto_anterior = db.session.query(rEmpleadoConcepto).filter(
        and_(
            rEmpleadoConcepto.idConcepto.in_(conceptos_a_eliminar),
            rEmpleadoConcepto.idPersona == idPersona
        )
    ).delete()
    print(elimina_concepto_anterior)
    empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona, Activo = 1).first()
    

    
    nuevo_concepto_data = {}
    nuevo_concepto_data['idPersona'] = idPersona
    nuevo_concepto_data['idTipoConcepto'] = "P"
    nuevo_concepto_data['idConcepto'] = idConcepto

    concepto = db.session.query(kConcepto).filter_by(idTipoConcepto = nuevo_concepto_data['idTipoConcepto'], idConcepto = idConcepto, idTipoEmpleado = empleado.idTipoEmpleado).first()
    
    nuevo_concepto_data['Porcentaje'] = concepto.Porcentaje
    nuevo_concepto_data['Monto'] = concepto.Monto
    nuevo_concepto_data['NumeroContrato'] = 1
    nuevo_concepto_data['FechaInicio'] = None
    nuevo_concepto_data['FechaFin'] = None
    nuevo_concepto_data['PagoUnico'] = 0


    nuevo_concepto = rEmpleadoConcepto(**nuevo_concepto_data)
    print("Nuevo concepto prima quinquenal")
    db.session.add(nuevo_concepto)

    # Realizar cambios en la base de datos
    db.session.commit()

def elimina_vacaciones_vencidas():
    hoy = datetime.today().date()
    if hoy == datetime(hoy.year, 7, 1).date(): # hoy == 1 julio:
        dias_personas = db.session.query(rDiasPersona).all()
        for dias_persona in dias_personas:
            dias_persona.DiasGanados = 0
        print("Dias ganados puestos a 0")
        db.session.commit()
    


def verificar_antiguedad_articulo_37_todos():

    empleadoPuesto = db.session.query(rEmpleadoPuesto).filter(rEmpleadoPuesto.idEstatusEP == 1).all()
    aniversario = False
    for puesto in empleadoPuesto:
        hoy = datetime.today().date()

        # revisar licencias que estén transcurriendo
        licencia = db.session.query(rSancionPersona).filter(
            and_(
                rSancionPersona.FechaInicio <= hoy,
                rSancionPersona.FechaFin >= hoy,
                rSancionPersona.idPersona == puesto.idPersona
            )
        ).first()
        
        if licencia is not None:
            print("Licencia en transición")
            
            empleado = db.session.query(rEmpleado).filter_by(idPersona = puesto.idPersona).first()

            if empleado is not None:
                # Obtener y ordenar los puestos del empleado
                puestos_empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona=puesto.idPersona).order_by(rEmpleadoPuesto.FechaTermino).all()

                # Encontrar el puesto activo
                puesto_activo = next((puesto for puesto in puestos_empleado if puesto.idEstatusEP == 1), None)
                if puesto_activo:
                    # Verificar que la FechaTermino del puesto activo sea None o mayor al día actual
                    if puesto_activo.FechaTermino is None or puesto_activo.FechaTermino > datetime.today().date():
                        fecha_inicio_consecutiva_mas_antigua = puesto_activo.FechaInicio
                    # Verificar la continuidad de los puestos
                        for puesto in puestos_empleado:
                            if puesto.FechaTermino == fecha_inicio_consecutiva_mas_antigua - timedelta(days=1):
                                fecha_inicio_consecutiva_mas_antigua = puesto.FechaInicio
                    else:
                        fecha_inicio_consecutiva_mas_antigua = None
                        print("Error: La fecha término del puesto ya ha transcurrido.")

                    fecha_inicio = fecha_inicio_consecutiva_mas_antigua
                else:
                    print("No se encontró un puesto Activo")
                    
            else:
                print("Empleado no encontrado")
                
            # Si es el aniversario del empleado
            if (fecha_inicio.month, fecha_inicio.day) == (hoy.month, hoy.day):
                print("Es aniversario del empleado con idPersona:" + str(puesto.idPersona))
                # Calcular la antigüedad en años completos
                antiguedad_en_anios = hoy.year - fecha_inicio.year
            
                descuentos = {}
                # Determinar el concepto correspondiente basado en los años de antigüedad
                if antiguedad_en_anios < 1:
                    descuentos["PorcentajePagado1"] = 100
                    descuentos["PorcentajePagado2"] = 50
                    descuentos["DiasPagados1"] = 15
                    descuentos["DiasPagados2"] = 15
                elif (1 <= antiguedad_en_anios < 5):
                    descuentos["PorcentajePagado1"] = 100
                    descuentos["PorcentajePagado2"] = 50
                    descuentos["DiasPagados1"] = 30
                    descuentos["DiasPagados2"] = 30
                elif (5 <= antiguedad_en_anios < 10):

                    descuentos["PorcentajePagado1"] = 100
                    descuentos["PorcentajePagado2"] = 50
                    descuentos["DiasPagados1"] = 45
                    descuentos["DiasPagados2"] = 45
                elif (10 <= antiguedad_en_anios):

                    descuentos["PorcentajePagado1"] = 100
                    descuentos["PorcentajePagado2"] = 50
                    descuentos["DiasPagados1"] = 60
                    descuentos["DiasPagados2"] = 60

                print("Descuentos e intervalos de tiempo calculados")
                
                licencia_ori = licencia.__dict__
                licencia_dict = licencia_ori.copy()
                licencia_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
                licencia_dict["idSancionPersona"] =  None
                print("licencia a diccionario")
                print(licencia_dict)
                
                idPersona = licencia_dict['idPersona']

                fechas = {}

                if isinstance(licencia_dict['FechaInicio'], date):
                    fechas["inicio_licencia_actual"] = licencia_dict['FechaInicio']
                    fechas["inicio_periodo"] = licencia_dict['FechaInicio']
                else:
                    fechas["inicio_licencia_actual"] = licencia_dict['FechaInicio'].date()
                    fechas["inicio_periodo"] = licencia_dict['FechaInicio'].date()

                if isinstance(licencia_dict['FechaInicio'], date):
                    fechas["fin_licencia_actual"] = licencia_dict['FechaFin']
                    fechas["fin_periodo"] = licencia_dict['FechaFin']
                else:
                    fechas["fin_licencia_actual"] = licencia_dict['FechaFin'].date()
                    fechas["fin_periodo"] = licencia_dict['FechaFin'].date()

                
                licencias_previas = db.session.query(rSancionPersona).filter_by(idPersona=puesto.idPersona).order_by(rSancionPersona.FechaInicio).all()

                for licencia_previa in licencias_previas:
                    print("licencia_previa")
                    print(licencia_previa.FechaInicio, licencia_previa.FechaFin)
                    
                    # Verificar que la fecha de inicio_periodo no esté dentro del rango de fechas anteriores o sea consecutiva
                    if (licencia_previa.FechaInicio <= fechas["inicio_periodo"] <= licencia_previa.FechaFin) or (licencia_previa.FechaFin == fechas["inicio_periodo"] - timedelta(days=1)):
                        fechas["inicio_periodo"] = licencia_previa.FechaInicio
                        
                        if licencia_previa.FechaInicio <= fechas["inicio_licencia_actual"] <= licencia_previa.FechaFin:
                            fechas["inicio_licencia_actual"] = licencia_previa.FechaFin + timedelta(days=1)

                    # Verificar que la fecha de fin_periodo no esté dentro del rango de fechas anteriores o sea consecutiva
                    if (licencia_previa.FechaInicio <= fechas["fin_periodo"] <= licencia_previa.FechaFin) or (licencia_previa.FechaInicio == fechas["fin_periodo"] + timedelta(days=1)):
                        fechas["fin_licencia_actual"] = licencia_previa.FechaInicio - timedelta(days=1)
                        fechas["fin_periodo"] = licencia_previa.FechaFin
                print("fechas")
                print(fechas)
                elimina = db.session.query(rSancionPersona).filter(
                    rSancionPersona.idPersona == idPersona,
                    rSancionPersona.idSancion == 2,
                    rSancionPersona.FechaInicio <= fechas["fin_periodo"],
                    rSancionPersona.FechaFin >= fechas["inicio_periodo"]
                ).delete()
                print("elimina")
                print(elimina)
                    
                dias_desc1 = int(descuentos["DiasPagados1"])
                dias_desc2 = int(descuentos["DiasPagados2"])

                dias_periodo = (fechas["fin_periodo"] - fechas["inicio_periodo"]).days + 1
                dias_permitidos = dias_desc1 + dias_desc2

                licencia_dict["FechaInicio"] = fechas["inicio_periodo"]
                licencia_dict["idPorcentaje"] = descuentos["PorcentajePagado1"]
                
                if dias_periodo <= dias_desc1:
                    licencia_dict["FechaFin"] = fechas["fin_periodo"]
                    guardar_art37(licencia_dict)
                else:
                    licencia_dict["FechaFin"] = fechas["inicio_periodo"] + timedelta(days=dias_desc1 - 1)
                    guardar_art37(licencia_dict)

                    licencia_dict["FechaInicio"] = licencia_dict["FechaFin"] +  timedelta(days=1)
                    if dias_periodo > dias_permitidos:
                        licencia_dict["FechaFin"] =  licencia_dict["FechaInicio"] + timedelta(days=dias_desc2)
                        licencia_dict["idPorcentaje"] = descuentos["PorcentajePagado2"]
                        guardar_art37(licencia_dict)


                        licencia_dict["FechaInicio"] = licencia_dict["FechaFin"] +  timedelta(days=1)
                        licencia_dict["FechaFin"] = fechas["fin_periodo"]
                        licencia_dict["idPorcentaje"] = 0 # Sin pago
                        guardar_art37(licencia_dict)


                    else:
                        licencia_dict["FechaFin"] =  fechas["fin_periodo"]
                        licencia_dict["idPorcentaje"] = descuentos["PorcentajePagado2"]
                        guardar_art37(licencia_dict)

                print("Se actualizó el artículo 37")

def guardar_art37(sancion_data):
    print("GUARDANDO SANCION" + str(sancion_data["idPersona"]))
    nueva_sancion = None

    print("sancion_data")
    print(sancion_data)
    sancion_data.pop('FechaCreacion', None)
    nueva_sancion = rSancionPersona(**sancion_data)
    db.session.add(nueva_sancion)
        
    # Realizar cambios en la base de datos
    db.session.commit()