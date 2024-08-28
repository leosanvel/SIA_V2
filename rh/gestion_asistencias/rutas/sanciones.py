from .gestion_asistencias import gestion_asistencias
from flask import render_template, request, session, jsonify
from catalogos.modelos.modelos import *
from app import db
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from rh.gestion_empleados.modelos.empleado import rEmpleadoPuesto, rEmpleado
from rh.gestion_asistencias.modelos.modelos import rSancionPersona
from general.modelos.modelos import tBitacora
from sqlalchemy import and_, or_
from datetime import date, datetime, timedelta


@gestion_asistencias.route('/rh/gestion-asistencias/sanciones', methods = ['POST', 'GET'])
def gestiona_sanciones():
    TipoSancion = db.session.query(kTipoSancion).filter_by(Activo = 1).all()
    Porcentajes = db.session.query(kPorcentajes).filter_by(Activo = 1).order_by(kPorcentajes.idPorcentaje.asc()).all()
    return render_template('/Sanciones.html', title='Licencias',
                           current_user = current_user,
                           TipoSancion = TipoSancion,
                           Porcentajes = Porcentajes)


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
            calcula_periodo_art37(sancion_data, descuentos_data)
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
                calcula_periodo_art37(sancion_data, descuentos_data)
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

            sancion_dict = sancion.__dict__
            sancion_dict.pop("_sa_instance_state", None)  # Eliminar atributo de SQLAlchemy
            sancion_dict["NumeroEmpleado"] = empleado.NumeroEmpleado
            sancion_dict["TipoSancion"] = "SANCION"
            sancion_dict["Porcentaje"] = 1
            
            
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
        
        # Calcular los días de las licencias dentro del periodo correcto
        total_dias = 0
        for licencia in licencias_anuales:
            fecha_inicio = max(licencia.FechaInicio, aniversario_anterior)
            
            fecha_fin = min(licencia.FechaFin, próximo_aniversario)
           
            dias_licencia = (fecha_fin - fecha_inicio).days + 1  # +1 para incluir ambos días

            total_dias += dias_licencia
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




def reparte_dias_totales(fechas, licencia, descuentos):


    elimina = db.session.query(rSancionPersona).filter(
        rSancionPersona.idPersona == licencia["idPersona"],
        rSancionPersona.idSancion == 2,
        rSancionPersona.FechaInicio <= fechas["fin_periodo"],
        rSancionPersona.FechaFin >= fechas["inicio_periodo"]
    ).delete()

        
    dias_desc1 = int(descuentos["DiasDisponibles1"])
    dias_desc2 = int(descuentos["DiasDisponibles2"])

    dias_periodo = (fechas["fin_periodo"] - fechas["inicio_periodo"]).days + 1
    dias_permitidos = dias_desc1 + dias_desc2

    licencia["FechaInicio"] = fechas["inicio_periodo"]
    licencia["idPorcentaje"] = descuentos["PorcentajePagado1"]
    
    if dias_permitidos == 0:
        licencia["idPorcentaje"] = 0
        guardar_o_modificar_sancion(licencia)
    else:
        if dias_periodo <= dias_desc1:
            licencia["FechaFin"] = fechas["fin_periodo"]
            guardar_o_modificar_sancion(licencia)
        else:
            licencia["FechaFin"] = fechas["inicio_periodo"] + timedelta(days=dias_desc1 - 1)
            guardar_o_modificar_sancion(licencia)

            licencia["FechaInicio"] = licencia["FechaFin"] +  timedelta(days=1)
            if dias_periodo > dias_permitidos:
                licencia["FechaFin"] =  licencia["FechaInicio"] + timedelta(days=dias_desc2)
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
                guardar_o_modificar_sancion(licencia)


                licencia["FechaInicio"] = licencia["FechaFin"] +  timedelta(days=1)
                licencia["FechaFin"] = fechas["fin_periodo"]
                licencia["idPorcentaje"] = 0 # Sin pago
                guardar_o_modificar_sancion(licencia)


            else:
                licencia["FechaFin"] =  fechas["fin_periodo"]
                licencia["idPorcentaje"] = descuentos["PorcentajePagado2"]
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