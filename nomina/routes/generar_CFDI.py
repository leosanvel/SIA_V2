from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .routes import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *

from rh.gestion_empleados.modelos.empleado import TPersona, BancoPersona, Empleado
from rh.gestion_empleados.modelos.domicilio import rDomicilio

import os, zipfile


@nomina.route('/nomina/generar-cfdi', methods = ['POST', 'GET'])
@permisos_de_consulta
def generar_CFDI():
    Quincenas = db.session.query(Quincena).all()
    return render_template('/generarCFDI.html', title='Generar CFDI',
                           Quincenas = Quincenas,
                           )

@nomina.route('/Nomina/crearCFDI', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_CFDI():
    
    strQuincena = request.form.get("NumQuincena")
    Quincenas = db.session.query(Quincena).filter_by(idQuincena = strQuincena).first()
    strMes = Quincenas.FechaInicio.strftime("%m")
    strAnio = Quincenas.FechaInicio.strftime("%y")
    # Definir la ruta y nombre del archivo
    nombre_archivo = nombre_carpeta = strMes + strQuincena + strAnio
    directorio = "nomina/CFDI/" + nombre_carpeta + "/"
    #lista para guardar las rutas y crear el ZIP
    rutas_archivos = []
    
    if os.path.isfile(directorio + nombre_archivo + ".zip"):
        respuesta = "existente"
    else:
        respuesta = "creado"
        os.makedirs(directorio)
        
        empleados_activos = db.session.query(Empleado.idPersona).filter_by(Activo=1).all()
            # Extrae los números de empleado de la lista de tuplas
        empleados_activos = [numero[0] for numero in empleados_activos]

        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%dT%H:%M:%S")
        consecutivo = 0

        for idPersona in empleados_activos:
            Persona = db.session.query(TPersona).filter_by(idPersona = idPersona).first()
            Nombre_completo = Persona.ApPaterno + " " + Persona.ApMaterno + " " + Persona.Nombre

            domicilioFiscal = db.session.query(rDomicilio).filter_by(idTipoDomicilio=2, idPersona = Persona.idPersona).first()
            if domicilioFiscal:
                CodigoPostal = str(domicilioFiscal.idCP)
            else:
                CodigoPostal = "NO REGISTRADO"


            Banco_persona = db.session.query(BancoPersona).filter_by(idPersona = Persona.idPersona, Activo = 1).first()
            if Banco_persona:
                CLABE = Banco_persona.Clabe
            else:
                CLABE = "NO REGISTRADA"


            #Falta generar: 
            NumeroEmpleado = "NoEmpleado"
            idCentroCosto = "idCentroCosto"
            idPuesto = "idPuesto"
            correoPersonal = "CORREO"
            consecutivo = consecutivo + 1
            NumQui = "X"
            TotalEmpP = "X"
            TotalEmpD = "X"
            TotalEmp = "X"
            FECPAGA = "X"
            FECINI = "X"
            FECFIN = "X"
            DIAS = "X"
            CVEISSSTE = "X"
            FECALTA = "X"
            PlazaSemana = "X"
            TotalBruto = "X"
            TOTALDIARIO = "X"

            PYD = "X"
            CVECONCEPTO = "X"
            IMPORTE = "X"
            TotalEmpDD = "X"
            TotalEmpDU = "X"

            Nombre_archivo = "I0" + str(consecutivo) + ".txt"
            ruta_completa = directorio + Nombre_archivo
            rutas_archivos.append(ruta_completa)
            Observaciones = "OBSERVACIONES"
            Descripcion = "DESCRIPCIÓN"
            
            with open(ruta_completa, "w") as archivo:
                archivo.write("Lote|7.0\n" )
                archivo.write("DOCUMENTO|CFDI_4.0|SI|SI|Recibo Nomina|ID_CONTROL|" + NumQui + "|ENVIO_RECEPTOR|" + Nombre_completo + "|" + correoPersonal + "|DATOSDECONTROL|DATODECONTROL|FILENAME|INAES_I00" + str(consecutivo) + "_" + NumQui + "_" + Persona.RFC + "\n")
                archivo.write("COMPROBANTE|4.0|NOM-INS|I00109256|" + fecha_hora_formateada + "|99|||" + TotalEmpP + "|" + TotalEmpD + "|MXN||" + TotalEmp + "|N|01|PUE|04100|\n" )
                archivo.write("EMISOR|CGP911204QU3|INSTITUTO NACIONAL DE LA ECONOMIA SOCIAL|603\n" )
                archivo.write("RECEPTOR|" + Persona.RFC + "|" + Nombre_completo + "|" + "|" + CodigoPostal + "|MEX||605|CN01\n" )
                archivo.write("CONCEPTO|84111505||1|ACT||Pago de nómina|" + TotalEmpP + "|" + TotalEmpP + "|" + TotalEmpD + "|03\n" )
                archivo.write("COMPLEMENTO|Nomina12|O|" + FECPAGA + "|" + FECINI + "|" + FECFIN + "|" + DIAS + "|" + TotalEmpP + "|" + TotalEmpD + "|\n" )
                archivo.write("COMPLEMENTO|Nomina12|EMISOR||0002099093|\n" )
                archivo.write("COMPLEMENTO|Nomina12|RECEPTOR|" + Persona.CURP + "|" + CVEISSSTE + "|" + FECALTA + "|P" + PlazaSemana + "W|02|No|01|02|" + NumeroEmpleado + "|" + idCentroCosto + "|" + idPuesto + "|1|04||" + CLABE + "|" + TotalBruto + "|" + TOTALDIARIO + "|DIF\n" )
            
                # if abreAux(strAux) then
                archivo.write("COMPLEMENTO|Nomina12|PERCEPCIONES|" + TotalEmpP + "|||" + TotalEmpP + "|0.00\n")
                # do until rsAux.eof
                archivo.write("COMPLEMENTO|Nomina12|PERCEPCION|" + PYD + "|P000_" + CVECONCEPTO + "|" + Descripcion + "|" + IMPORTE + "|0.00\n")
                # if abreAux(strAux) then
                archivo.write("COMPLEMENTO|Nomina12|DEDUCCIONES|" + TotalEmpDD + "|" + TotalEmpDU + "\n")
                # do until rsAux.eof
                archivo.write("COMPLEMENTO|Nomina12|DEDUCCION|" + PYD + "|D000_" + CVECONCEPTO + "|" + Descripcion + "|" + IMPORTE + "\n")


                archivo.write("COMPLEMENTO|Nomina12|OTROSPAGO \n")
                archivo.write("COMPLEMENTO|Nomina12|OTROPAGO|002|S000_SUE|Subsidio al Empleo informativo|0.00 \n")
                archivo.write("COMPLEMENTO|Nomina12|SUBSIDIOALEMPLEO|0.00 \n")
                archivo.write("IMPRESION|TABLA|LEYINAES|ATRIBUTO|" + Observaciones + "| \n")
                archivo.write("TABLA|DEPNOMINA|ATRIBUTO|DescripNomina|" + Descripcion +"\n")
                archivo.write("TABLA|FormaPago|ATRIBUTO|FormadePago|PUE Pago en una sola exhibición \n")
                archivo.write("TABLA|MetodPago|ATRIBUTO|MetododePago|TRANSFERENCIA ELECTRONICA \n")


        crea_zip(rutas_archivos, directorio, nombre_carpeta)
    return jsonify({"url_descarga": url_for('nomina.descargar_cfdi_zip', nombre_archivo=nombre_carpeta), "respuesta":respuesta})
    # return jsonify({"respuesta":"creado"})

def crea_zip(rutas, destino , nombre_archivo): # Crear un archivo ZIP
    with zipfile.ZipFile(destino + nombre_archivo +".zip", "w") as zipf:
        # Agregar cada archivo al archivo ZIP
        for ruta_archivo in rutas:
            zipf.write(ruta_archivo, os.path.basename(ruta_archivo))

@nomina.route('/Nomina/descargar_cfdi_zip/<nombre_archivo>')
def descargar_cfdi_zip(nombre_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "nomina", "CFDI", nombre_archivo)
    return send_from_directory(directory=directorio_archivos, path=nombre_archivo+ ".zip", as_attachment=True)