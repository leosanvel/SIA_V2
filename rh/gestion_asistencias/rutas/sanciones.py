from .gestion_asistencias import gestion_asistencias
from flask import render_template, request, session, jsonify
from catalogos.modelos.modelos import *
from app import db
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from rh.gestion_empleados.modelos.empleado import rEmpleadoPuesto, rEmpleado
from rh.gestion_asistencias.modelos.modelos import rSancionPersona
from nomina.modelos.modelos import tNomina
from general.modelos.modelos import tBitacora
from sqlalchemy import and_, or_
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd


@gestion_asistencias.route('/rh/gestion-asistencias/sanciones', methods = ['POST', 'GET'])
def gestiona_sanciones():
    TipoSancion = db.session.query(kTipoSancion).filter_by(Activo = 1).all()
    Porcentajes = db.session.query(kPorcentajes).filter_by(Activo = 1).order_by(kPorcentajes.idPorcentaje.asc()).all()
    Quincenas = quincenas = db.session.query(kQuincena).all()
    return render_template('/Sanciones.html', title='Licencias',
                           current_user = current_user,
                           TipoSancion = TipoSancion,
                           Porcentajes = Porcentajes,
                           Quincenas = Quincenas)

@gestion_asistencias.route("/rh/gestion-asistencias/verificar-dias", methods = ["POST"])
def verficar_dias():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idSancionPersona' : 'idSancionPersona',
        'idPersona' : 'idPersona',
        'idSancion' : 'idSancion',
        'idPorcentaje' : 'idPorcentaje',
        'FechaInicio' : 'FechaInicio',
        'FechaFin' : 'FechaFin',
        'Descripcion' : 'Descripcion',
        'Quincena': 'idQuincena',
    }
    sancion_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    mapeo_descuentos = { #NombreEnFormulario : nombreEnBase
                    'DiasPagados1' : 'DiasPagados1',
                    'PorcentajePagado1' : 'PorcentajePagado1',
                    'DiasDisponibles1' : 'DiasDisponibles1',
                    'DiasPagados2' : 'DiasPagados2',
                    'PorcentajePagado2' : 'PorcentajePagado2',
                    'DiasDisponibles2' : 'DiasDisponibles2',
                }
    descuentos_data = {mapeo_descuentos[key]: request.form.get(key) for key in mapeo_descuentos.keys()}

    fechasConsecutivas = request.form.get("checkFechasConsecutivas") # (True or None)
    if fechasConsecutivas:
        sancion_data['FechaInicio'] = datetime.strptime(sancion_data['FechaInicio'], '%d/%m/%Y')
        sancion_data['FechaFin'] = datetime.strptime(sancion_data['FechaFin'], '%d/%m/%Y')
        if sancion_data['idSancion'] == '2' or sancion_data["idSancion"] == '4': #Artículo 37
            print("Articulo37")

    return jsonify({"guardado": True})

@gestion_asistencias.route('/rh/gestion-asistencias/guardar-sancion', methods = ['POST'])
def guarda_Sancion():
    mapeo_nombres = { #NombreEnFormulario : nombreEnBase
        'idSancionPersona' : 'idSancionPersona',
        'idPersona' : 'idPersona',
        'idSancion' : 'idSancion',
        'idPorcentaje' : 'idPorcentaje',
        'FechaInicio' : 'FechaInicio',
        'FechaFin' : 'FechaFin',
        'Descripcion' : 'Descripcion',
        'NumQuincena': 'idQuincena',
    }
    sancion_data = {mapeo_nombres[key]: request.form.get(key) for key in mapeo_nombres.keys()}

    mapeo_descuentos = { #NombreEnFormulario : nombreEnBase
                    'DiasPagados1' : 'DiasPagados1',
                    'PorcentajePagado1' : 'PorcentajePagado1',
                    'DiasDisponibles1' : 'DiasDisponibles1',
                    'DiasPagados2' : 'DiasPagados2',
                    'PorcentajePagado2' : 'PorcentajePagado2',
                    'DiasDisponibles2' : 'DiasDisponibles2',
                }
    descuentos_data = {mapeo_descuentos[key]: request.form.get(key) for key in mapeo_descuentos.keys()}
    
    fechasConsecutivas = request.form.get("checkFechasConsecutivas") # (True or None)
    if fechasConsecutivas:
        sancion_data['FechaInicio'] = datetime.strptime(sancion_data['FechaInicio'], '%d/%m/%Y')
        sancion_data['FechaFin'] = datetime.strptime(sancion_data['FechaFin'], '%d/%m/%Y')
        if sancion_data['idSancion'] == '2' or sancion_data["idSancion"] == '4': #Artículo 37
            #calcula_periodo_art37(sancion_data, descuentos_data)
            calcular_periodo_articulo_37(sancion_data, descuentos_data)
            print("Artículo 37")
        else:
            guardar_o_modificar_sancion(sancion_data)
    else:
        FechasFlatpickr = request.form.get("FechasFlatpickr")
        fechas = FechasFlatpickr.split(',')  # Separa las fechas por comas
        for fecha in fechas:
            fecha = fecha.strip() #Quita espacios en blanco
            sancion_data['FechaInicio'] = datetime.strptime(fecha, '%d/%m/%Y')
            sancion_data['FechaFin'] = datetime.strptime(fecha, '%d/%m/%Y')
            
            if sancion_data['idSancion'] == '2' or sancion_data["idSancion"] == '4': #Artículo 37
                #calcula_periodo_art37(sancion_data, descuentos_data)
                #reparte_dias(sancion_data, descuentos_data)
                print("Artículo 37")
            else:
                guardar_o_modificar_sancion(sancion_data)
    return jsonify(sancion_data)

def guardar_o_modificar_sancion(sancion_data):
    nueva_sancion = None
    try:
        sancion_a_modificar = db.session.query(rSancionPersona).filter(rSancionPersona.idSancionPersona == sancion_data["idSancionPersona"]).one()
        # Actualizar los atributos de 'sancion_existente' con los valores de 'sancion_data'
        sancion_a_modificar.update(**sancion_data)
        #for attr, value in sancion_data.items():
        #    if not attr.startswith('_') and hasattr(sancion_a_modificar, attr):
        #        setattr(sancion_a_modificar, attr, value)

        guardar_modificar_licencia = 5
                
    except NoResultFound:
        ultimo_id_sancion_persona = db.session.query(func.max(rSancionPersona.idSancionPersona)).scalar()
        if ultimo_id_sancion_persona is None:
            sancion_data["idSancionPersona"] = 1
        else:
            sancion_data["idSancionPersona"] = ultimo_id_sancion_persona + 1
        nueva_sancion = rSancionPersona(**sancion_data)
        db.session.add(nueva_sancion)

        guardar_modificar_licencia = 4

    ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
    if ultimo_idBitacora is None:
        idBitacora = 1
    else:
        idBitacora = ultimo_idBitacora + 1

    nueva_bitacora = tBitacora(idBitacora=idBitacora,
                               idTipoMovimiento=guardar_modificar_licencia,
                               idUsuario=current_user.idPersona)
    
    db.session.add(nueva_bitacora)
        
    # Realizar cambios en la base de datos
    db.session.commit()
    print("Fecha fin descuento guardado: ", nueva_sancion.FechaFinDescuento)

@gestion_asistencias.route('/rh/gestion-asistencias/buscar-sancion', methods = ['POST'])
def busca_Sancion():
    idPersona = request.form.get('idPersona')
    
    BuscaFechaInicio = request.form.get('BuscaFechaInicio')
    BuscaFechaFin = request.form.get('BuscaFechaFin')
 
    query = db.session.query(rSancionPersona)
    if idPersona:
        query = query.filter(rSancionPersona.idPersona == int(idPersona))
    if BuscaFechaInicio:
        BuscaFechaInicio = datetime.strptime(BuscaFechaInicio, '%d/%m/%Y')
        query = query.filter(rSancionPersona.FechaInicio >= BuscaFechaInicio)

    if BuscaFechaFin:
        BuscaFechaFin = datetime.strptime(BuscaFechaFin, '%d/%m/%Y')
        query = query.filter(rSancionPersona.FechaInicio <= BuscaFechaFin)

        
    # Si todas las variables están vacías, no se aplican filtros y se devuelve una lista vacía
    if not (idPersona or BuscaFechaInicio or BuscaFechaFin):
        sanciones = []
    else:
        sanciones = query.all()

    lista_sanciones = []
    for sancion in sanciones:
        if sancion is not None:
            try:
                empleado = db.session.query(rEmpleado).filter(rEmpleado.idPersona == sancion.idPersona, rEmpleado.Activo==1).one()

            except NoResultFound:
                print("Empleado no encontrado")

            quincena = db.session.query(kQuincena).filter_by(idQuincena = sancion.idQuincena).first()

            sancion_dict = sancion.__dict__
            sancion_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            sancion_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
            sancion_dict["TipoSancion"] = "SANCION"
            sancion_dict["Porcentaje"] = 1

            if quincena is not None:
                sancion_dict["Quincena"] = quincena.Descripcion
            else:
                sancion_dict["Quincena"] = ""
            
            
            lista_sanciones.append(sancion_dict)

    lista_tipos = []
    TipoSancion = db.session.query(kTipoSancion).filter_by(Activo = 1).all()
    for tipo in TipoSancion:
        if tipo is not None:
            tipo_dict = tipo.__dict__
            tipo_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_tipos.append(tipo_dict)

    lista_porcentajes = []
    Porcentajes = db.session.query(kPorcentajes).filter_by(Activo = 1).all()
    for porcentaje in Porcentajes:
        if porcentaje is not None:
            porcentaje_dict = porcentaje.__dict__
            porcentaje_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            lista_porcentajes.append(porcentaje_dict)

    return jsonify({
        'sanciones': lista_sanciones,
        'tiposSancion': lista_tipos,
        'porcentajes': lista_porcentajes
    })

@gestion_asistencias.route('/rh/gestion-empleados/eliminar-sancion', methods = ['POST'])
def eliminar_Sanciones():
    idSancionPersona = request.form.get("idSancionPersona")
    try:
        Sancion = db.session.query(rSancionPersona).get(idSancionPersona)

        db.session.delete(Sancion)

        ultimo_idBitacora = db.session.query(func.max(tBitacora.idBitacora)).scalar()
        if ultimo_idBitacora is None:
            idBitacora = 1
        else:
            idBitacora = ultimo_idBitacora + 1

        nueva_bitacora = tBitacora(idBitacora=idBitacora,
                               idTipoMovimiento=6,
                               idUsuario=current_user.idPersona)
        
        db.session.add(nueva_bitacora)

        db.session.commit()

    except NoResultFound:
        print("No se encontró sanción")

    return jsonify({"eliminado": True})

@gestion_asistencias.route('/rh/gestion-empleados/cancela_sancion', methods = ['POST', 'GET'])
def cancela_sancion():
    idSancionPersona = request.form.get('idSancionPersona')
    SancionPersona = db.session.query(rSancionPersona).filter_by(idSancionPersona = idSancionPersona).first()
    if SancionPersona is not None:
        SancionPersona_dict = SancionPersona.__dict__
        SancionPersona_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
        return jsonify(SancionPersona_dict)
    else:
        return jsonify(False)

    
@gestion_asistencias.route('/rh/gestion-asistencias/calculo-dias-articulo-37', methods = ['POST'])
def calculo_dias_articulo_37():
    idPersona = request.form.get("idPersona")

    fecha_inicio_consecutiva_mas_antigua = calcula_fecha_consecutiva_puestos(idPersona)
    resultado = {}
    if fecha_inicio_consecutiva_mas_antigua is not None:
    
        hoy = date.today()

        # Calcular la diferencia en días
        diferencia_dias = (hoy - fecha_inicio_consecutiva_mas_antigua).days

        # # Convertir la diferencia en semanas
        # diferencia_semanas = diferencia_dias / 7

        
        # if diferencia_semanas > (52*10):  #52 semanas * 10 años
        if diferencia_dias > (365*10):  #365 dias * 10 años
            resultado["PorcentajePagado1"] = 100
            resultado["PorcentajePagado2"] = 50
            resultado["DiasPagados1"] = 60
            resultado["DiasPagados2"] = 60
        elif diferencia_dias > (365*5):  # 5 años
            resultado["PorcentajePagado1"] = 100
            resultado["PorcentajePagado2"] = 50
            resultado["DiasPagados1"] = 45
            resultado["DiasPagados2"] = 45
        elif diferencia_dias > (365):  # 1 año
            resultado["PorcentajePagado1"] = 100
            resultado["PorcentajePagado2"] = 50
            resultado["DiasPagados1"] = 30
            resultado["DiasPagados2"] = 30
        else:   #menos de 1 año
            resultado["PorcentajePagado1"] = 100
            resultado["PorcentajePagado2"] = 50
            resultado["DiasPagados1"] = 15
            resultado["DiasPagados2"] = 15

        resultado["FechaInicioPuesto"] = fecha_inicio_consecutiva_mas_antigua

        # Calcular el aniversario anterior y el próximo aniversario
        año_actual = hoy.year
        aniversario_anterior = fecha_inicio_consecutiva_mas_antigua.replace(year=año_actual)
        if aniversario_anterior > hoy:
            aniversario_anterior = aniversario_anterior.replace(year=año_actual - 1)
        próximo_aniversario = aniversario_anterior.replace(year=aniversario_anterior.year + 1)
        
        # Buscar licencias que se solapan con el periodo de interés
        licencias_anuales = db.session.query(rSancionPersona).filter(
            rSancionPersona.idPersona == idPersona,
            or_(rSancionPersona.idSancion == 2, rSancionPersona.idSancion == 4),
            (rSancionPersona.FechaInicio <= próximo_aniversario) &
            (rSancionPersona.FechaFin >= aniversario_anterior)
        ).order_by(rSancionPersona.FechaFin.desc()).all()

        # Obtener los días festivos
        dias_festivos = db.session.query(kDiasFestivos.Fecha).all()
        dias_festivos_lista = [item[0] for item in dias_festivos]
        
        # Calcular los días de las licencias dentro del periodo correcto
        total_dias = 0
        for licencia in licencias_anuales:
            fecha_inicio = licencia.FechaInicioDescuento #max(licencia.FechaInicio, aniversario_anterior)
            
            fecha_fin = licencia.FechaFinDescuento #min(licencia.FechaFin, próximo_aniversario)
           
            #dias_licencia = np.busday_count(fecha_inicio, fecha_fin, holidays=dias_festivos_lista) + 1 # +1 para incluir ambos días, ignora días festivos y fines de semana
            dias_licencia = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir ambos días

            total_dias += int(dias_licencia)
        print("total_dias")
        print(total_dias)
        resta = resultado["DiasPagados1"] - total_dias
        if (resta > 0):
            resultado["DiasDisponibles1"] = resta
            total_dias =  0
        else:
            resultado["DiasDisponibles1"] = 0
            total_dias = total_dias - resultado["DiasPagados1"]

        resta = resultado["DiasPagados2"] - total_dias
        if (resta > 0):
            resultado["DiasDisponibles2"] = resta
            total_dias =  0
        else:
            resultado["DiasDisponibles2"] = 0
            total_dias = total_dias - resultado["DiasPagados2"]

        print(resultado)






    else:
        resultado["Error"] = True
    return jsonify(resultado)




def calcula_periodo_art37(licencia, descuentos):
    idPersona = licencia['idPersona']
    idSancion = licencia['idSancion']
    print("licencia['idPersona']")
    print(licencia['idPersona'])
    print("licencia['idSancion']")
    print(licencia['idSancion'])
    
    licencias_previas = db.session.query(rSancionPersona).filter_by(idPersona=idPersona).order_by(rSancionPersona.FechaFin.desc()).all()
    print(licencias_previas)
    fechas = {}


    fechas["inicio_licencia_actual"] = licencia['FechaInicio'].date()
    fechas["inicio_periodo"] = licencia['FechaInicio'].date()

    fechas["fin_licencia_actual"] = licencia['FechaFin'].date()
    fechas["fin_periodo"] = licencia['FechaFin'].date()
   
    
    for licencia_previa in licencias_previas:
        # Verificar que la fecha de licencia['FechaInicio'] no esté dentro del rango de fechas anteriores
        if (licencia_previa.FechaInicio <= fechas["inicio_periodo"] <= licencia_previa.FechaFin) or (licencia_previa.FechaFin == fechas["inicio_periodo"] - timedelta(days=1)) :

            if (licencia_previa.FechaInicio <= fechas["inicio_licencia_actual"] <= licencia_previa.FechaFin):

                fechas["inicio_licencia_actual"] = licencia_previa.FechaFin + timedelta(days=1)
            fechas["inicio_periodo"] = licencia_previa.FechaInicio

        if (licencia_previa.FechaInicio <= fechas["fin_periodo"] <= licencia_previa.FechaFin) or (licencia_previa.FechaInicio == fechas["fin_periodo"] + timedelta(days=1)) :

            fechas["fin_licencia_actual"] = licencia_previa.FechaInicio - timedelta(days=1)
            fechas["fin_periodo"] = licencia_previa.FechaFin


    reparte_dias_totales(fechas, licencia, descuentos)
    return 0

def calcular_periodo_articulo_37(licencia, descuentos):
    idPersona = licencia["idPersona"]
    Periodo = request.form.get("Periodo")
    print(Periodo)
    fecha_inicio_consecutiva_mas_antigua = calcula_fecha_consecutiva_puestos(idPersona)
    hoy = datetime.now()
    FechaLimiteInf = None
    FechaLimiteSup = None

    # Calcular el aniversario anterior y el próximo aniversario
    año_actual = hoy.year
    aniversario = fecha_inicio_consecutiva_mas_antigua.replace(year=año_actual)

    if licencia["FechaInicio"].date() < aniversario:
        print("Antes")
        aniversario_anterior = aniversario.replace(year=año_actual - 1)
        FechaLimiteInf = aniversario_anterior
        FechaLimiteSup = aniversario

    elif licencia["FechaInicio"].date() > aniversario:
        print("Despues")
        aniversario_siguiente = aniversario.replace(year=año_actual + 1)
        FechaLimiteInf = aniversario
        FechaLimiteSup = aniversario_siguiente

    # Buscar licencias que se solapan con el periodo de interés
    licencias_anuales = db.session.query(rSancionPersona).filter(
        rSancionPersona.idPersona == idPersona,
        or_(rSancionPersona.idSancion == 2, rSancionPersona.idSancion == 4),
        (rSancionPersona.FechaInicio >= FechaLimiteInf) &
        (rSancionPersona.FechaFin < FechaLimiteSup)
    ).order_by(rSancionPersona.FechaFin.desc()).all()

    total_dias = 0
    for licencia_anual in licencias_anuales:
        fecha_inicio = licencia_anual.FechaInicioDescuento
        fecha_fin = licencia_anual.FechaFinDescuento
        dias_licencia = (fecha_fin - fecha_inicio).days + 1

        total_dias += int(dias_licencia)

    print("Total dias")
    print(total_dias)

    resta = int(descuentos["DiasPagados1"]) - total_dias
    if resta > 0:
        DiasDisponibles1 = resta
        total_dias = 0
    else:
        DiasDisponibles1 = 0
        total_dias = total_dias - int(descuentos["DiasPagados1"])

    resta = int(descuentos["DiasPagados2"]) - total_dias
    if resta > 0:
        DiasDisponibles2 = resta
        total_dias = 0
    else:
        DiasDisponibles2 = 0
        total_dias = total_dias - int(descuentos["DiasPagados2"])

    print(DiasDisponibles1, DiasDisponibles2)
    descuentos["DiasDisponibles1"] = DiasDisponibles1
    descuentos["DiasDisponibles2"] = DiasDisponibles2
    reparte_dias(licencia, descuentos)

def calcular_periodo_artículo_37_1(licencia, descuentos):
    idPersona = licencia["idPersona"]
    fecha_inicio_consecutiva_mas_antigua = calcula_fecha_consecutiva_puestos(idPersona)
    hoy = datetime.now()
    FechasInicio = []
    FechasFin = []
    FechasLimiteInf = []
    FechasLimiteSup = []

    # Calcular el aniversario anterior y el próximo aniversario
    año_actual = hoy.year               
    aniversario = fecha_inicio_consecutiva_mas_antigua.replace(year=año_actual)

    if licencia["FechaFin"].date() < aniversario:
        print("Antes")
        aniversario_anterior = aniversario.replace(year=año_actual - 1)
        FechasLimiteInf.append(aniversario_anterior)
        FechasLimiteSup.append(aniversario)
        FechasInicio.append(licencia["FechaInicio"])
        FechasFin.append(licencia["FechaFin"])

    elif licencia["FechaInicio"].date() > aniversario:
        print("Despues")
        aniversario_siguiente = aniversario.replace(year=año_actual + 1)
        FechasLimiteInf.append(aniversario)
        FechasLimiteSup.append(aniversario_siguiente)
        FechasInicio.append(licencia["FechaInicio"])
        FechasFin.append(licencia["FechaFin"])

    else:
        if licencia["FechaInicio"].date() <= aniversario <= licencia["FechaFin"].date():
            print("Entre")
            aniversario_anterior = aniversario.replace(year=año_actual - 1)
            aniversario_siguiente = aniversario.replace(year=año_actual + 1)
            FechasLimiteInf.append(aniversario_anterior)
            FechasLimiteSup.append(aniversario)
            FechasInicio.append(licencia["FechaInicio"])
            FechasFin.append(datetime.combine(aniversario, datetime.min.time()) - timedelta(days=1))

            FechasLimiteInf.append(aniversario)
            FechasLimiteSup.append(aniversario_siguiente)
            FechasInicio.append(datetime.combine(aniversario, datetime.min.time()))
            FechasFin.append(licencia["FechaFin"])
            

    for FechaLimiteInf, FechaLimiteSup, FechaInicio, FechaFin in zip(FechasLimiteInf, FechasLimiteSup,FechasInicio, FechasFin):
        # Buscar licencias que se solapan con el periodo de interés
        licencias_anuales = db.session.query(rSancionPersona).filter(
            rSancionPersona.idPersona == idPersona,
            or_(rSancionPersona.idSancion == 2, rSancionPersona.idSancion == 4),
            (rSancionPersona.FechaInicio >= FechaLimiteInf) &
            (rSancionPersona.FechaFin < FechaLimiteSup)
        ).order_by(rSancionPersona.FechaFin.desc()).all()

        total_dias = 0
        for licencia_1 in licencias_anuales:
            fecha_inicio = max(licencia_1.FechaInicio, aniversario_anterior)
            fecha_fin = min(licencia_1.FechaFin, aniversario)
            dias_licencia = (fecha_fin - fecha_inicio).days + 1

            total_dias += int(dias_licencia)

        print("Total dias")
        print(total_dias)

        resta = int(descuentos["DiasPagados1"]) - total_dias
        if resta > 0:
            DiasDisponibles1 = resta
            total_dias = 0
        else:
            DiasDisponibles1 = 0
            total_dias = total_dias - int(descuentos["DiasPagados1"])

        resta = int(descuentos["DiasPagados2"]) - total_dias
        if resta > 0:
            DiasDisponibles2 = resta
            total_dias = 0
        else:
            DiasDisponibles2 = 0
            total_dias = total_dias - int(descuentos["DiasPagados2"])

        print(DiasDisponibles1, DiasDisponibles2)
        licencia["FechaInicio"] = FechaInicio
        licencia["FechaFin"] = FechaFin
        descuentos["DiasDisponibles1"] = DiasDisponibles1
        descuentos["DiasDisponibles2"] = DiasDisponibles2
        reparte_dias(licencia, descuentos)

def reparte_dias(licencia, descuentos):
    dias = (licencia["FechaFin"]  - licencia["FechaInicio"]).days + 1
    print("Días")
    print(dias)

    dias_desc1 = int(descuentos["DiasDisponibles1"])
    dias_desc2 = int(descuentos["DiasDisponibles2"])
    dias_permitidos = dias_desc1 + dias_desc2

    if dias_permitidos == 0:
        licencia["idPorcentaje"] = 1
        reparte_quincenas(licencia, descuentos)
    else:
        if dias_desc1 > 0:
            if dias <= dias_desc1:
                licencia["idSancion"] = 4
                licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
                print(licencia)
                reparte_quincenas(licencia, descuentos)
            else:
                dias_extra = dias - dias_desc1
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_desc1 - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 4
                licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
                print(licencia)
                reparte_quincenas(licencia, descuentos)

                licencia["FechaInicio"] = licencia["FechaFin"] + timedelta(days=1)
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_extra - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                print(licencia)
                reparte_quincenas(licencia, descuentos)
        else:
            if dias <= dias_desc2:
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                print(licencia)
                reparte_quincenas(licencia, descuentos)
            else:
                dias_extra = dias - dias_desc2
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_desc2 - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                print(licencia)
                reparte_quincenas(licencia, descuentos)

                licencia["FechaInicio"] = licencia["FechaFin"] + timedelta(days=1)
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_extra - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = 1
                print(licencia)
                reparte_quincenas(licencia, descuentos)

def reparte_quincenas(licencia, descuentos):
    dias = (licencia["FechaFin"] - licencia["FechaInicio"]).days + 1
    print("Días: ", dias)

    quincena_inicio = licencia["idQuincena"]
    Quincena_licencia = False

    ultima_licencia = db.session.query(rSancionPersona).filter(
        rSancionPersona.idPersona == licencia["idPersona"],
        or_(rSancionPersona.idSancion == 2, rSancionPersona.idSancion == 4)
    ).order_by(rSancionPersona.idSancionPersona.desc()).first()

    nomina_disponible = db.session.query(tNomina).filter_by(Estatus = 1).order_by(tNomina.FechaInicial.asc()).first()
    if nomina_disponible is None:
        nomina_disponible = db.session.query(tNomina).filter_by(Estatus = 2).order_by(tNomina.FechaInicial.desc()).first()
        Nomina_procesada = True
    else:
        Nomina_procesada = False

    if ultima_licencia is not None:
        if nomina_disponible.FechaFinal <= ultima_licencia.FechaFinDescuento:
            Quincena_licencia = True

    if Quincena_licencia is True:
        quincena_inicio = db.session.query(kQuincena).filter(kQuincena.FechaInicio <= ultima_licencia.FechaFinDescuento, kQuincena.FechaFin >= ultima_licencia.FechaFinDescuento).first()
        if ultima_licencia.FechaFinDescuento == quincena_inicio.FechaFin:
            quincena_inicio = db.session.query(kQuincena).get(quincena_inicio.idQuincena + 1)
        
    else:
        if Nomina_procesada is False:
            quincena_inicio = db.session.query(kQuincena).filter_by(FechaInicio = nomina_disponible.FechaInicial, FechaFin = nomina_disponible.FechaFinal).first()
        else:
            quincena_inicio = db.session.query(kQuincena).filter(kQuincena.FechaInicio > nomina_disponible.FechaInicial, kQuincena.FechaFin > nomina_disponible.FechaFinal).order_by(kQuincena.idQuincena.asc()).first()

    cont = 0

    print("Quincena inicio: ", quincena_inicio)
    print("Ultima Licencia: ", ultima_licencia)

    while dias > 0 and cont < 366:
        print("cont")
        print(cont)

        if cont == 0:
            if Quincena_licencia is True:
                licencia["FechaInicioDescuento"] = ultima_licencia.FechaFinDescuento + timedelta(days=1)
            else:
                if quincena_inicio.FechaInicio <= licencia["FechaInicio"].date() <= quincena_inicio.FechaFin:
                    licencia["FechaInicioDescuento"] = licencia["FechaInicio"].date()
                else:
                    licencia["FechaInicioDescuento"] = quincena_inicio.FechaInicio
        else:
            licencia["FechaInicioDescuento"] = quincena_inicio.FechaInicio

        # if Quincena_licencia is True:
        #     print("Es de licencia")
        #     if quincena_inicio.FechaInicio <= ultima_licencia.FechaFinDescuento < quincena_inicio.FechaFin:
        #         if cont == 0:
        #             print("Ultima fecha es de licencia y entra por primera vez")
        #             print(ultima_licencia)
        #             licencia["FechaInicioDescuento"] = ultima_licencia.FechaFinDescuento + timedelta(days=1)
        #     else:
        #         if ultima_licencia.FechaFinDescuento == quincena_inicio.FechaFin:
        #             print("Ultima fecha de licencia es igual a ultimo día de quincena")
        #             quincena_inicio = db.session.query(kQuincena).get(quincena_inicio.idQuincena + 1)
        #             licencia["FechaInicioDescuento"] = quincena_inicio.FechaInicio
        #         elif "FechaFinDescuento" in licencia:
        #             if quincena_inicio.FechaInicio <= licencia["FechaFinDescuento"] <= quincena_inicio.FechaFin:
        #                 print("Tomando la fecha fin descuento anterior")
        #                 licencia["FechaInicioDescuento"] = licencia["FechaFinDescuento"] + timedelta(days=1)
        #         else:
        #             print("Tomando la fecha inicio de la quincena")
        #             licencia["FechaInicioDescuento"] = quincena_inicio.FechaInicio

        # else:
        #     print("Es de nómina")
        #     if quincena_inicio.FechaInicio <= licencia["FechaInicio"].date() <= quincena_inicio.FechaFin:
        #         print("La Fecha Inicio de la licencia está dentro de la quincena de nómina")
        #         licencia["FechaInicioDescuento"] = licencia["FechaInicio"].date()
        #     else:
        #         if "FechaFinDescuento" in licencia:
        #             if quincena_inicio.FechaInicio <= licencia["FechaFinDescuento"] <= quincena_inicio.FechaFin:
        #                 licencia["FechaInicioDescuento"] = licencia["FechaFinDescuento"] + timedelta(days=1)
        #         else:
        #             print("Fecha inicio es fecha inicio de quincena")
        #             licencia["FechaInicioDescuento"] = quincena_inicio.FechaInicio

        # if Quincena_licencia is True and cont == 0:
        #     if quincena_inicio.FechaFin == ultima_licencia.FechaFinDescuento:
        #         quincena_inicio = db.session.query(kQuincena).get(quincena_inicio.idQuincena + 1)
        #     else:
        #         licencia["FechaInicioDescuento"] = ultima_licencia.FechaFinDescuento + timedelta(days=1)

        dias_quincena = (quincena_inicio.FechaFin - licencia["FechaInicioDescuento"]).days + 1
        if (dias_quincena < dias):
            licencia["FechaFinDescuento"] = quincena_inicio.FechaFin
        else:
            licencia["FechaFinDescuento"] = licencia["FechaInicioDescuento"] + timedelta(days=dias - 1)

        licencia["idQuincena"] = quincena_inicio.idQuincena
        licencia["idSancionPersona"] = None
        licencia["Dias"] = (licencia["FechaFinDescuento"] - licencia["FechaInicioDescuento"]).days + 1
        print(licencia)

        guardar_o_modificar_sancion(licencia)

        dias = dias - ((licencia["FechaFinDescuento"] - licencia["FechaInicioDescuento"]).days + 1)

        if licencia["FechaFinDescuento"] == quincena_inicio.FechaFin:
            quincena_inicio = db.session.query(kQuincena).filter_by(idQuincena = quincena_inicio.idQuincena + 1).first()

        cont = cont + 1
        print("cont")
        print(cont)


def reparte_dias_1(licencia, descuentos):
    idPersona = licencia["idPersona"]
    # Obtener los días festivos
    dias_festivos = db.session.query(kDiasFestivos.Fecha).all()
    dias_festivos_lista = [item[0] for item in dias_festivos]

    #dias = np.busday_count(licencia["FechaInicio"].date(), licencia["FechaFin"].date(), holidays=dias_festivos_lista) + 1
    dias = (licencia["FechaFin"]  - licencia["FechaInicio"]).days + 1
    print("Días")
    print(dias)

    #aniversario = aniversario_anterior.replace(year=aniversario_anterior.year + 1)

    dias_desc1 = int(descuentos["DiasDisponibles1"])
    dias_desc2 = int(descuentos["DiasDisponibles2"])
    dias_permitidos = dias_desc1 + dias_desc2

    if dias_permitidos == 0:
        licencia["idPorcentaje"] = 1
        guardar_o_modificar_sancion(licencia)
    else:
        if dias_desc1 > 0:
            if dias <= dias_desc1:
                print(type(licencia))
                licencia["idSancion"] = 4
                licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
                guardar_o_modificar_sancion(licencia)
            else:
                dias_extra = dias - dias_desc1
                print("Días extra")
                print(dias_extra)
                #fecha_aux = pd.bdate_range(start=licencia["FechaInicio"], periods=dias_desc1, holidays=dias_festivos_lista, freq="C")
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_desc1 - 1)
                print("Fecha aux")
                print(fecha_aux)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 4
                licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
                guardar_o_modificar_sancion(licencia)

                licencia["FechaInicio"] = licencia["FechaFin"] + timedelta(days=1)
                #fecha_aux = pd.bdate_range(start=licencia["FechaInicio"], periods=dias_extra, holidays=dias_festivos_lista, freq="C")
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_extra - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                guardar_o_modificar_sancion(licencia)
        else:
            if dias <= dias_desc2:
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                guardar_o_modificar_sancion(licencia)
            else:
                dias_extra = dias - dias_desc2
                #fecha_aux = pd.bdate_range(start=licencia["FechaInicio"], periods=dias_desc2, holidays=dias_festivos_lista, freq="C")
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_desc2 - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                guardar_o_modificar_sancion(licencia)

                licencia["FechaInicio"] = licencia["FechaFin"] + timedelta(days=1)
                #fecha_aux = pd.bdate_range(start=licencia["FechaInicio"], periods=dias_extra, holidays=dias_festivos_lista, freq="C")
                fecha_aux = licencia["FechaInicio"] + timedelta(days=dias_extra - 1)
                licencia["FechaFin"] = fecha_aux
                licencia["idSancion"] = 2
                licencia["idPorcentaje"] = 1
                guardar_o_modificar_sancion(licencia)


def reparte_dias_totales(fechas, licencia, descuentos):


    elimina = db.session.query(rSancionPersona).filter(
        rSancionPersona.idPersona == licencia["idPersona"],
        or_(rSancionPersona.idSancion == 2, rSancionPersona.idSancion == 4),
        rSancionPersona.FechaInicio <= fechas["fin_periodo"],
        rSancionPersona.FechaFin >= fechas["inicio_periodo"]
    ).delete()

        
    dias_desc1 = int(descuentos["DiasDisponibles1"])
    dias_desc2 = int(descuentos["DiasDisponibles2"])

    # Obtener los días festivos
    dias_festivos = db.session.query(kDiasFestivos.Fecha).all()
    dias_festivos_lista = [item[0] for item in dias_festivos]

    dias_periodo = np.busday_count(fechas["inicio_periodo"], fechas["fin_periodo"], holidays=dias_festivos_lista) + 1 # +1 para incluir ambos días, ignora días festivos y fines de semana

    dias_permitidos = dias_desc1 + dias_desc2

    licencia["FechaInicio"] = fechas["inicio_periodo"]
    licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
    
    if dias_permitidos == 0:
        licencia["idPorcentaje"] = 0
        guardar_o_modificar_sancion(licencia)
    else:
        if dias_periodo <= dias_desc1:
            licencia["FechaFin"] = fechas["fin_periodo"]
            licencia["idSancion"] = 4
            guardar_o_modificar_sancion(licencia)
        else:
            #licencia["FechaFin"] = fechas["inicio_periodo"] + timedelta(days=dias_desc1 - 1)
            fechas_aux = pd.bdate_range(start=fechas["inicio_periodo"], periods=int(descuentos["DiasPagados1"]), holidays=dias_festivos_lista, freq="C")
            licencia["FechaFin"] = fechas_aux[-1]
            print("Fecha Fin Dias 100")
            print(licencia["FechaFin"])
            licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
            licencia["idSancion"] = 4
            guardar_o_modificar_sancion(licencia)

            licencia["FechaInicio"] = licencia["FechaFin"] + timedelta(days=1)
            if dias_periodo > dias_permitidos:
                #licencia["FechaFin"] =  licencia["FechaInicio"] + timedelta(days=dias_desc2)
                fechas_aux = pd.bdate_range(start=licencia["FechaInicio"], periods=int(descuentos["DiasPagados2"]), holidays=dias_festivos_lista, freq="C")
                licencia["FechaFin"] = fechas_aux[-1]
                print("Fecha Fin Dias 50")
                print(licencia["FechaFin"])
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                licencia["idSancion"] = 2
                guardar_o_modificar_sancion(licencia)


                licencia["FechaInicio"] = licencia["FechaFin"] +  timedelta(days=1)
                licencia["FechaFin"] = fechas["fin_periodo"]
                print("Fecha Fin Dias 0")
                print(licencia["FechaFin"])
                licencia["idPorcentaje"] = 0 # Sin pago
                licencia["idSancion"] = 2
                guardar_o_modificar_sancion(licencia)


            else:
                licencia["FechaFin"] =  fechas["fin_periodo"]
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                licencia["idSancion"] = 2
                guardar_o_modificar_sancion(licencia)


def calcula_fecha_consecutiva_puestos(idPersona):
    # puestos_empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona).all()
    empleado = db.session.query(rEmpleado).filter_by(idPersona = idPersona).first()

    if empleado is not None:
        # Obtener y ordenar los puestos del empleado
        puestos_empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona=idPersona).order_by(rEmpleadoPuesto.FechaTermino.desc()).all()

        # Encontrar el puesto activo
        puesto_activo = next((puesto for puesto in puestos_empleado if puesto.idEstatusEP == 1), None)
        if puesto_activo:
            # Verificar que la FechaTermino del puesto activo sea None o mayor al día actual
            if puesto_activo.FechaTermino is None or puesto_activo.FechaTermino > datetime.today().date():
                fecha_inicio_consecutiva_mas_antigua = puesto_activo.FechaInicio
               # Verificar la continuidad de los puestos
                for puesto in puestos_empleado:
                    if (puesto.FechaTermino == fecha_inicio_consecutiva_mas_antigua - timedelta(days=1) or puesto.FechaTermino == fecha_inicio_consecutiva_mas_antigua) and puesto.FechaTermino is not None:
                        fecha_inicio_consecutiva_mas_antigua = puesto.FechaInicio
            else:
                fecha_inicio_consecutiva_mas_antigua = None
                print("Error: La fecha término del puesto ya ha transcurrido.")

            return fecha_inicio_consecutiva_mas_antigua
        else:
            print("No se encontró un puesto Activo")
            return None
    else:
        print("Empleado no encontrado")
        return None