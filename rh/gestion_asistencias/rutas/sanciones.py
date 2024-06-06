from .gestion_asistencias import gestion_asistencias
from flask import render_template, request, session, jsonify
from catalogos.modelos.modelos import *
from app import db
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from rh.gestion_empleados.modelos.empleado import rEmpleadoPuesto, rEmpleado
from rh.gestion_asistencias.modelos.modelos import rSancionPersona
from sqlalchemy import and_
from datetime import date, datetime, timedelta



@gestion_asistencias.route('/rh/gestion-asistencias/sanciones', methods = ['POST', 'GET'])
def gestiona_sanciones():
    TipoSancion = db.session.query(kTipoSancion).filter_by(Activo = 1).all()
    Porcentajes = db.session.query(kPorcentajes).filter_by(Activo = 1).all()
    return render_template('/Sanciones.html', title='Licencias',
                           current_user=current_user,
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


    fechasConsecutivas = request.form.get("checkFechasConsecutivas") # (True or None)
    if fechasConsecutivas:
        sancion_data['FechaInicio'] = datetime.strptime(sancion_data['FechaInicio'], '%d/%m/%Y')
        sancion_data['FechaFin'] = datetime.strptime(sancion_data['FechaFin'], '%d/%m/%Y')
        if sancion_data['idSancion'] == '2': #Artículo 37
                mapeo_descuentos = { #NombreEnFormulario : nombreEnBase
                    'DiasPagados1' : 'DiasPagados1',
                    'PorcentajePagado1' : 'PorcentajePagado1',
                    'DiasPagados2' : 'DiasPagados2',
                    'PorcentajePagado2' : 'PorcentajePagado2',
                }
                descuentos_data = {mapeo_descuentos[key]: request.form.get(key) for key in mapeo_descuentos.keys()}
                condicionales_articulo_37(sancion_data, descuentos_data)
        else:
            guardar_o_modificar_sancion(sancion_data)
    else:
        FechasFlatpickr = request.form.get("FechasFlatpickr")
        fechas = FechasFlatpickr.split(',')  # Separa las fechas por comas
        for fecha in fechas:
            fecha = fecha.strip() #Quita espacios en blanco
            sancion_data['FechaInicio'] = datetime.strptime(fecha, '%d/%m/%Y')
            sancion_data['FechaFin'] = datetime.strptime(fecha, '%d/%m/%Y')
            
            if sancion_data['idSancion'] == '2': #Artículo 37
                condicionales_articulo_37(sancion_data, descuentos_data)
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
                
    except NoResultFound:
        nueva_sancion = rSancionPersona(**sancion_data)
        db.session.add(nueva_sancion)
        
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
    puesto_empleado = db.session.query(rEmpleadoPuesto).filter_by(idPersona = idPersona, idEstatusEP = 1).first()
    
    if puesto_empleado is not None:
        fecha_inicio = puesto_empleado.FechaInicio # tipo datetime.date
        print("fecha_inicio")
        print(fecha_inicio)
        hoy = date.today()

        # Calcular la diferencia en días
        diferencia_dias = (hoy - fecha_inicio).days

        # Convertir la diferencia en semanas
        diferencia_semanas = diferencia_dias / 7

        resultado = {}
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

        resultado["FechaInicioPuesto"] = fecha_inicio


        print(str(resultado["DiasPagados1"])+" días al " + str(resultado["PorcentajePagado1"]) + "%")
        print(str(resultado["DiasPagados2"])+" días al " + str(resultado["PorcentajePagado2"]) + "%")
        print("Después sin pago")
        return jsonify(resultado)
            
    return jsonify({"Error":True})


def condicionales_articulo_37(licencia, descuentos):
    idPersona = licencia['idPersona']
    idSancion = licencia['idSancion']
    
    licencias_previas = db.session.query(rSancionPersona).filter_by(idPersona=idPersona, idSancion=idSancion).order_by(rSancionPersona.FechaFin.desc()).all()
    fechas = {}

    fechas["inicio_licencia_actual"] = licencia['FechaInicio'].date()
    fechas["inicio_periodo"] = licencia['FechaInicio'].date()
    fechas["fin_periodo"] = licencia['FechaFin'].date()
    fechas["fin_licencia_actual"] = licencia['FechaFin'].date()
    
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

    
    # if dias_totales < dias_consecutivos_anteriores:
    #     elimina anteriores

    descuento_keys = sorted([key for key in descuentos.keys() if key.startswith("DiasPagados")])
    for dias_descuento in descuento_keys:

        dias_periodo = (fechas["fin_periodo"] - fechas["inicio_periodo"]).days + 1
        if dias_periodo > 0:
            print("Descuento" + dias_descuento[-1])
    
            porcentaje_key = f"PorcentajePagado{dias_descuento[-1]}"
            
            licencia["FechaInicio"] = fechas["inicio_periodo"]
            print("int(descuentos[dias_descuento])")
            print(int(descuentos[dias_descuento]))
            if int(descuentos[dias_descuento]) < dias_periodo:
                print("CAso1")
                fecha_fin = fechas["inicio_periodo"] + timedelta(days=int(descuentos[dias_descuento]) - 1)
                licencia["FechaFin"] = fecha_fin
                fechas["inicio_periodo"] = fecha_fin + timedelta(days=1)
            else:
                print("Caso2")
                licencia["FechaFin"] =  fechas["fin_periodo"]
                fechas["inicio_periodo"] = fechas["fin_periodo"] + timedelta(days=1)

            licencia["idPorcentaje"] = descuentos[porcentaje_key]
            print("licencia")
            print(licencia)
            guardar_o_modificar_sancion(licencia)
            
    dias_periodo = (fechas["fin_periodo"] - fechas["inicio_periodo"]).days + 1
    if dias_periodo > 0:
        licencia["FechaInicio"] = fechas["inicio_periodo"]
        licencia["FechaFin"] = fechas["fin_periodo"]
        licencia["idPorcentaje"] = 0
        guardar_o_modificar_sancion(licencia)

        print("dias_periodo")
        print(dias_periodo)
    else:
        print("dias_periodo")
        print(dias_periodo)



        