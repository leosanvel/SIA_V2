from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from autenticacion.modelos.modelos import *

from rh.gestion_empleados.modelos.empleado import tPersona, rBancoPersona, rSerieNomina, rEmpleado, rEmpleadoPuesto, tPuesto
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from prestaciones.modelos.modelos import rEmpleadoConcepto
from nomina.modelos.modelos import *

import os, zipfile

@nomina.route('/nomina/generar-cfdi', methods = ['POST', 'GET'])
@permisos_de_consulta

def generar_CFDI():
    Nominas = db.session.query(tNomina).filter_by(Estatus=2).all()
    return render_template('/generarCFDI.html', title='Generar CFDI',
                           Nominas = Nominas,
                           )

@nomina.route('/Nomina/crearCFDI', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_CFDI():    
    
    numero_nomina = request.form.get("idNomina")
    numero_serie = 0
    Nomina = db.session.query(tNomina).filter_by(idNomina=numero_nomina,Estatus=2).first()
    if Nomina:
        numero_quincena = Nomina.Quincena
        mes_pago = Nomina.FechaPago.strftime("%m")
        anio_pago = Nomina.FechaPago.strftime("%Y")
        fecha_pago = Nomina.FechaPago
        fecha_inicial = Nomina.FechaInicial
        fecha_final = Nomina.FechaFinal
        observaciones_nomina = Nomina.Observaciones
        descripcion_nomina = Nomina.Descripcion
        nombre_carpeta = numero_quincena + mes_pago + anio_pago 
        directorio = "nomina/Doctos/" + nombre_carpeta
        if not os.path.exists(directorio):
            os.mkdir(directorio)
        directorio = directorio + "/CFDI/"
        if not os.path.exists(directorio):
            os.mkdir(directorio)

        rutas_archivos = []

        serienomina = db.session.query(rSerieNomina).filter_by().first()
        if serienomina:
            numero_serie = serienomina.SerieFinal
        
        Empleados = db.session.query(rEmpleado).filter_by().all()
        for Empleado in Empleados:
            empleado_nomina = 0
            nombre_empleado = ""
            correo_empleado = ""
            rfc_empleado = ""
            total_percepciones = 0
            total_deducciones = 0
            codigo_postal = ""
            dias_trabajados = 0
            curp_empleado = ""
            numero_issste = ""
            fecha_alta_issste = ""
            numero_semanas = 99
            numero_empleado = 0
            centro_costos = ""
            codigo_plaza = "" 
            clabe_interbancaria=0
            salario_bruto = 0
            salario_diario= 0
            descuento_impuesto = 0

            NominaEmpleado = db.session.query(rNominaPersonas).filter_by(idPersona=Empleado.idPersona).all()
            for EmpleadoNomina in NominaEmpleado:
                empleado_nomina = 1
                if EmpleadoNomina.idTipoConcepto == "P":
                    total_percepciones = total_percepciones + EmpleadoNomina.Importe
                    if EmpleadoNomina.idConcepto == "DT":
                        dias_trabajados = EmpleadoNomina.Importe
                elif EmpleadoNomina.idTipoConcepto == "D":
                    total_deducciones = total_deducciones + (EmpleadoNomina.Importe * -1)
                    if EmpleadoNomina.idConcepto == "1":
                        descuento_impuesto = EmpleadoNomina.Importe * -1
            if empleado_nomina == 1:
                numero_serie = numero_serie + 1
                Persona = db.session.query(tPersona).filter_by(idPersona = Empleado.idPersona).first()
                if Persona:
                    nombre_empleado = Persona.ApPaterno + " " + Persona.ApMaterno + " " + Persona.Nombre
                    rfc_empleado = Persona.RFC
                    if Empleado.CorreoInstitucional != "":
                        correo_empleado = Empleado.CorreoInstitucional
                    elif Persona.CorreoPersonal != "":
                        correo_empleado = Persona.CorreoPersonal
                    curp_empleado = Persona.CURP
                
                DomicilioFiscal = db.session.query(rDomicilio).filter_by(idPersona=Empleado.idPersona,idTipoDomicilio=2).first()
                if DomicilioFiscal:
                    codigo_postal = str(DomicilioFiscal.idCP)

                numero_issste = Empleado.NoISSSTE
                fecha_alta_issste = Empleado.FecAltaISSSTE
                numero_empleado = Empleado.NumeroEmpleado

                EmpleadoP = db.session.query(rEmpleadoPuesto).filter_by(idPersona = Empleado.idPersona, idEstatusEP = 1).first()
                if EmpleadoP:        
                    Puestos = db.session.query(tPuesto).filter_by(ConsecutivoPuesto = EmpleadoP.idPuesto).first()
                    if Puestos:
                        CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = Puestos.idCentroCosto).first()
                        if CentroCosto:
                            centro_costos = CentroCosto.CentroCosto                    
                        Plaza = db.session.query(kPlazas).filter_by(idPlaza = Puestos.CodigoPresupuestal).first()
                        if Plaza:
                            codigo_plaza = Puestos.NivelSalarial + " " + Plaza.Plaza

                EmpleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto="P",idConcepto="7").first()
                if EmpleadoConcepto:
                    salario_diario = round(EmpleadoConcepto.Monto / 30,2)
                    salario_bruto = round(salario_diario * 15,2) 
                fecha_actual = datetime.now()
                fecha_generacion = fecha_actual.strftime("%Y-%m-%dT%H:%M:%S")
                nombre_archivo = "I0"+str(numero_serie)+".txt"
                ruta_completa = directorio + nombre_archivo
                
                if os.path.exists(ruta_completa): 
                    os.remove(ruta_completa)

                rutas_archivos.append(ruta_completa)            
                with open(ruta_completa, "w") as archivo:
#-------------------Encabezado                    
                    archivo.write("Lote|7.0\n" ) 
                    archivo.write("DOCUMENTO|CFDI_4.0|SI|SI|Recibo Nomina|ID_CONTROL|" + str(numero_quincena) + "|ENVIO_RECEPTOR|" + str(nombre_empleado) + "|" + str(correo_empleado) + "|DATOSDECONTROL|DATODECONTROL|FILENAME|INAES_I00" + str(numero_serie) + "_" + str(numero_quincena) + "_" + str(rfc_empleado) + "\n")
                    archivo.write("COMPROBANTE|4.0|NOM-INS|I00109256|" + str(fecha_generacion) + "|99|||" + str(total_percepciones) + "|" + str(total_deducciones) + "|MXN||" + str(total_percepciones - total_deducciones) + "|N|01|PUE|04100|\n" )
                    archivo.write("EMISOR|CGP911204QU3|INSTITUTO NACIONAL DE LA ECONOMIA SOCIAL|603\n" )
                    archivo.write("RECEPTOR|" + str(rfc_empleado) + "|" + str(nombre_empleado) + "|" + "|" + str(codigo_postal) + "|MEX||605|CN01\n" )
                    archivo.write("CONCEPTO|84111505||1|ACT||Pago de nómina|" + str(total_percepciones) + "|" + str(total_percepciones) + "|" + str(total_deducciones) + "|03\n" )
                    archivo.write("COMPLEMENTO|Nomina12|O|" + str(fecha_pago) + "|" + str(fecha_inicial) + "|" + str(fecha_final) + "|" + str(dias_trabajados) + "|" + str(total_percepciones) + "|" + str(total_deducciones) + "|\n" )
                    archivo.write("COMPLEMENTO|Nomina12|EMISOR||0002099093|\n" )
                    archivo.write("COMPLEMENTO|Nomina12|RECEPTOR|" + str(curp_empleado) + "|" + str(numero_issste) + "|" + str(fecha_alta_issste) + "|P" + str(numero_semanas) + "W|02|No|01|02|" + str(numero_empleado) + "|" + str(centro_costos) + "|" + str(codigo_plaza) + "|1|04||" + str(clabe_interbancaria) + "|" + str(salario_bruto) + "|" + str(salario_diario) + "|DIF\n" )
#-------------------Percepciones
                    clave_sat = ""
                    id_concepto = "" 
                    descripcion_concepto = ""
                    monto_concepto = 0                              
                    archivo.write("COMPLEMENTO|Nomina12|PERCEPCIONES|" + str(total_percepciones) + "|||" + str(total_percepciones) + "|0.00\n")
                    RecorrerPercepciones = db.session.query(rNominaPersonas).filter_by(idPersona= Empleado.idPersona, idTipoConcepto = "P").all()
                    for Percepcion in RecorrerPercepciones:
                        Concepto = db.session.query(kConcepto).filter_by(idTipoConcepto=Percepcion.idTipoConcepto, idConcepto = Percepcion.idConcepto).first()
                        if Concepto:
                            clave_sat = Concepto.ClaveSAT
                            id_concepto = Concepto.idConcepto 
                            descripcion_concepto = Concepto.Concepto 
                            monto_concepto = Percepcion.Importe
                            archivo.write("COMPLEMENTO|Nomina12|PERCEPCION|" + str(clave_sat) + "|P000_" + str(id_concepto) + "|" + str(descripcion_concepto) + "|" + str(monto_concepto) + "|0.00\n")            
#-------------------Deducciones
                    clave_sat = ""
                    id_concepto = "" 
                    descripcion_concepto = ""
                    monto_concepto = 0                
                    archivo.write("COMPLEMENTO|Nomina12|DEDUCCIONES|" + str(total_deducciones) + "|" + str(descuento_impuesto) + "\n")
                    RecorrerDeducciones = db.session.query(rNominaPersonas).filter_by(idPersona= Empleado.idPersona, idTipoConcepto = "D").all()
                    for Deduccion in RecorrerDeducciones:
                        Concepto = db.session.query(kConcepto).filter_by(idTipoConcepto = Deduccion.idTipoConcepto, idConcepto = Deduccion.idConcepto).first()
                        if Concepto:
                            clave_sat = Concepto.ClaveSAT
                            id_concepto = Concepto.idConcepto 
                            descripcion_concepto = Concepto.Concepto 
                            monto_concepto = (Deduccion.Importe * -1)
                            archivo.write("COMPLEMENTO|Nomina12|DEDUCCION|" + str(clave_sat) + "|D000_" + str(id_concepto) + "|" + str(descripcion_concepto) + "|" + str(monto_concepto) + "\n")
#-------------------Pie 

                    archivo.write("COMPLEMENTO|Nomina12|OTROSPAGO \n")
                    archivo.write("COMPLEMENTO|Nomina12|OTROPAGO|002|S000_SUE|Subsidio al Empleo informativo|0.00 \n")
                    archivo.write("COMPLEMENTO|Nomina12|SUBSIDIOALEMPLEO|0.00 \n")
                    archivo.write("IMPRESION|TABLA|LEYINAES|ATRIBUTO|" + str(observaciones_nomina) + "| \n")
                    archivo.write("TABLA|DEPNOMINA|ATRIBUTO|DescripNomina|" + str(descripcion_nomina) +"\n")
                    archivo.write("TABLA|FormaPago|ATRIBUTO|FormadePago|PUE Pago en una sola exhibición \n")
                    archivo.write("TABLA|MetodPago|ATRIBUTO|MetododePago|TRANSFERENCIA ELECTRONICA \n")
        respuesta = "1"    
    else:
        respuesta = "0"
        
    crea_zip(rutas_archivos, directorio, nombre_carpeta)
    return jsonify({"respuesta":respuesta,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo=nombre_carpeta+'.',extencion_archivo='zip'),})

def crea_zip(rutas, destino , nombre_archivo):
    with zipfile.ZipFile(destino + nombre_archivo +".zip", "w") as zipf:
        for ruta_archivo in rutas:
            zipf.write(ruta_archivo, os.path.basename(ruta_archivo))