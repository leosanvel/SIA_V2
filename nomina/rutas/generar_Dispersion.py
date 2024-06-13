from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from autenticacion.modelos.modelos import *
from nomina.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import tPersona, rEmpleado, rBancoPersona

import os

@nomina.route('/nomina/generar-dispersion', methods = ['POST', 'GET'])

def Dispersion():
    Nominas = db.session.query(tNomina).filter_by(Estatus=2).all()
    return render_template('/dispersion.html', title='Generar Dispersión',
                           Nominas=Nominas,
                           )

@nomina.route('/Nomina/Dispersion', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_Dispersion():
    respuesta = 0
    numero_nomina = request.form.get("idNomina")
    Nomina = db.session.query(tNomina).filter_by(idNomina=numero_nomina,Estatus=2).first()
    if Nomina:
        numero_quincena = Nomina.Quincena
        mes_pago = Nomina.FechaPago.strftime("%m")
        anio_pago = Nomina.FechaPago.strftime("%Y")
        nombre_carpeta = numero_quincena + mes_pago + anio_pago 
        directorio = "nomina/Doctos/" + nombre_carpeta + "/"

        if not os.path.exists(directorio):
            os.mkdir(directorio)

        nombre_archivo = "Dispersion.txt"
        ruta_completa = directorio + nombre_archivo
        
        if os.path.exists(ruta_completa): 
            os.remove(ruta_completa)

        with open(ruta_completa, "w") as archivo:
            
            

            tipo_registro = "01"
            consecutivo_registro = 1 #0000001
            codigo_operacion = "60"
            banco_participante = "167"
            sentido = "E"
            servicio = "2"
            consecutivo_bloque = "04"
            numero_bloque = str(Nomina.FechaPago.strftime("%d")) + "257" + consecutivo_bloque
            fecha_presentacion = Nomina.FechaPago.strftime("%Y") + Nomina.FechaPago.strftime("%m")+Nomina.FechaPago.strftime("%d")
            codigo_divisa = "01"
            causa_rechazo = "00"
            modalidad = "2"
            uso_futuro = "                                                                                                                                                                                                                                                                                                                                                                                                  "
            archivo.write(tipo_registro+str(consecutivo_registro).zfill(7)+codigo_operacion+banco_participante+sentido+servicio+str(numero_bloque)+str(fecha_presentacion)+codigo_divisa+causa_rechazo+modalidad+uso_futuro+"\n")

            NominaPersonas = db.session.query(rNominaPersonas.idPersona,func.sum(rNominaPersonas.Importe).label("Importe")).filter_by(idNomina=Nomina.idNomina).group_by(rNominaPersonas.idPersona).all()
            for NPersona in NominaPersonas:
                tipo_registro = "02"
                consecutivo_registro = consecutivo_registro + 1
                banco_receptor = ""
                importe = str(NPersona.Importe)
                importe = importe.replace(".","")
                importe = importe.zfill(15)
                uso_futuro = "                "
                tipo_operacion = "02"
                tipo_cuenta_ordenante = "40"
                numero_cuenta_ordenante = "00001180228001000108"
                nombre_ordenante = "TESORERIA DE LA FEDERACION              "
                rfc_ordenante = "SHC850101U37      "
                tipo_cuenta_receptor = "40"
                numero_cuenta_receptor = ""
                nombre_receptor = ""
                rfc_receptor = ""
                referencia_servicio = "                                        "
                nombre_titular_servicio = "                                        "
                importe_iva = "000000000000000"
                referencia_numerica_ordenante = ""
                referencia_leyenda_ordenante = Nomina.Descripcion
                clave_rastreo = ""
                motivo_devolucion = ""
                fecha_presentacion_inicial = ""
                solicitud_confirmacion = "1"
                uso_futuro_banco = "           " 

                Banco = db.session.query(rBancoPersona).filter_by(idPersona = NPersona.idPersona,Activo=1,Verificado=1).first()
                if Banco:
                    banco_receptor = Banco.Clabe[1:3]
                    numero_cuenta_receptor = str(Banco.Clabe).zfill(20)
                Empleado = db.session.query(tPersona).filter_by(idPersona=NPersona.idPersona).first()
                if Empleado:
                    nombre_receptor = Empleado.ApPaterno + " " + Empleado.ApMaterno + " " + Empleado.Nombre
                    rfc_receptor = Empleado.RFC                    
     
                archivo.write(tipo_registro+str(consecutivo_registro).zfill(7)+codigo_operacion+codigo_divisa+fecha_presentacion+banco_participante+banco_receptor+importe+uso_futuro+tipo_operacion+fecha_presentacion+tipo_cuenta_ordenante+numero_cuenta_ordenante+nombre_ordenante+rfc_ordenante+tipo_cuenta_receptor+numero_cuenta_receptor+nombre_receptor+rfc_receptor+referencia_servicio+nombre_titular_servicio+importe_iva+referencia_numerica_ordenante+referencia_leyenda_ordenante+clave_rastreo+motivo_devolucion+fecha_presentacion_inicial+solicitud_confirmacion+uso_futuro_banco+"\n")

        respuesta = "1"
        print("Proceso terminado")
    else:
        print("Sin registros")

    return jsonify({"respuesta":respuesta,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo='Dispersion.',extencion_archivo='txt'),})
