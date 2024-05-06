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

import os, zipfile

@nomina.route('/nomina/generar-cfdi', methods = ['POST', 'GET'])
@permisos_de_consulta

def generar_CFDI():
    Quincenas = db.session.query(kQuincena).order_by(kQuincena.idQuincena).all()
    return render_template('/generarCFDI.html', title='Generar CFDI',
                           Quincenas = Quincenas,
                           )

@nomina.route('/Nomina/crearCFDI', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_CFDI():
    
    strQuincena = request.form.get("NumQuincena")

    Quincenas = db.session.query(kQuincena).filter_by(idQuincena = strQuincena).first()
    strQuincena = str(Quincenas.Quincena)
    NumQuincena = Quincenas.Quincena
    strMes = Quincenas.FechaInicio.strftime("%m")
    strAnio = Quincenas.FechaInicio.strftime("%Y")
    desQuincena = Quincenas.Descripcion
    FECPAGA = Quincenas.FechaFin 
    FECINI = Quincenas.FechaInicio
    FECFIN = Quincenas.FechaFin

    if (NumQuincena % 2) == 0:
        NumQuincena = 0
    else:
        NumQuincena = 1

    Observaciones = request.form.get("Observaciones")
    
    Descripcion = "NOMINA FEDERAL DE LA " + desQuincena + " DE " + strAnio

    if len(strMes) == 1:
        strMes = "0" + strMes

    if len(strQuincena) == 1:
        strQuincena = "0" + strQuincena

    NumQui = "NQNA" + strQuincena + strAnio + "F"

    serienomina = db.session.query(rSerieNomina).filter_by().first()

    if serienomina:
        consecutivo = serienomina.SerieFinal
    else:
        consecutivo = 0

    print("Serie: ", consecutivo)
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
        
        Empleados = db.session.query(rEmpleado).filter_by(idPersona = 5574).all()

        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%dT%H:%M:%S")

        for Empleado in Empleados:

            Persona = db.session.query(tPersona).filter_by(idPersona = Empleado.idPersona).first()
            Nombre_completo = Persona.ApPaterno + " " + Persona.ApMaterno + " " + Persona.Nombre

            domicilioFiscal = db.session.query(rDomicilio).filter_by(idTipoDomicilio=2, idPersona = Persona.idPersona).first()
            if domicilioFiscal:
                CodigoPostal = str(domicilioFiscal.idCP)
            else:
                CodigoPostal = "NO REGISTRADO"

            Banco_persona = db.session.query(rBancoPersona).filter_by(idPersona = Persona.idPersona, Activo = 1).first()
            if Banco_persona:
                CLABE = Banco_persona.Clabe
            else:
                CLABE = "NO REGISTRADA"

            EmpleadoP = db.session.query(rEmpleadoPuesto).filter_by(idPersona = Empleado.idPersona, idEstatusEP = 1).first()
            Puestos = db.session.query(tPuesto).filter_by(ConsecutivoPuesto = EmpleadoP.idPuesto).first()
            CentroCosto = db.session.query(kCentroCostos).filter_by(idCentroCosto = Puestos.idCentroCosto).first()
            
            CC = CentroCosto.CentroCosto
            Plaza = db.session.query(Plazas).filter_by(idPlaza = Puestos.CodigoPresupuestal).first()
            CPlaza = Puestos.NivelSalarial + " " + Plaza.Plaza
            CVEISSSTE = str(Empleado.NoISSSTE)
            FECALTA = str(Empleado.FecAltaISSSTE)

            #Falta generar: 
            consecutivo += 1

            TotalEmpP = 0
            TotalEmpD = 0
            TotalEmpDD = 0
            TotalEmpDU = 0

            DIAS = 15

            PlazaSemana = "99" #Numero de semana fecha ingreso gob y fecha de paga
            TotalSueldoCG = 0
            TotalBruto = 0
            
            Conceptos = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona).all()
            for Concep in Conceptos:
            
                if Concep.idTipoConcepto == "P":
                    TotalEmpP = TotalEmpP + Concep.Monto
                    if Concep.idConcepto == "7" or Concep.idConcepto == "77" or Concep.idConcepto == "A1" or Concep.idConcepto == "A2" or Concep.idConcepto == "A3" or Concep.idConcepto == "A4" or Concep.idConcepto == "A5":
                        TotalBruto = TotalBruto + Concep.Monto                        
                    if Concep.idConcepto == "7" or Concep.idConcepto == "CG":
                        TotalSueldoCG = TotalSueldoCG + Concep.Monto

#calcular dias a descontar
            TOTALDIARIO = TotalBruto / DIAS
            TOTALDIARIO = "{:.2f}".format(TOTALDIARIO)

            for Concep in Conceptos:
                if Concep.idTipoConcepto == "D":                    
                    if Concep.idConcepto == "1":
                        


                        TotalEmpDU = TotalEmpDU + Concep.Monto #TOTAL DE CLAVE CONCEPTO 1
                    else:
                        if Concep.idConcepto == "77D":  
                            if NumQuincena == 0:
                                TotalEmpDD = TotalEmpDD + 7.27
                            else:
                                TotalEmpDD = TotalEmpDD + 7.28
                        else:
                            if Concep.Porcentaje > 0:
                                TotalEmpDD = TotalEmpDD + float((TotalBruto * Concep.Porcentaje) / 100)
                            else:
                                TotalEmpDD = TotalEmpDD + float(Concep.Monto) #IMPORTE DE PERCEPCION O DEDUCCION

            TotalEmpDD = "{:.2f}".format(TotalEmpDD)
             
            
            Nombre_archivo = "I0" + str(consecutivo) + ".txt"
            ruta_completa = directorio + Nombre_archivo
            rutas_archivos.append(ruta_completa)

            with open(ruta_completa, "w") as archivo:

                if len(str(Empleado.CorreoInstitucional)) == 0:
                    Correo = Persona.CorreoPersonal
                else:
                    Correo = Empleado.CorreoInstitucional

                archivo.write("Lote|7.0\n" )
                archivo.write("DOCUMENTO|CFDI_4.0|SI|SI|Recibo Nomina|ID_CONTROL|" + str(NumQui) + "|ENVIO_RECEPTOR|" + str(Nombre_completo) + "|" + str(Correo) + "|DATOSDECONTROL|DATODECONTROL|FILENAME|INAES_I00" + str(consecutivo) + "_" + str(NumQui) + "_" + str(Persona.RFC) + "\n")
                archivo.write("COMPROBANTE|4.0|NOM-INS|I00109256|" + str(fecha_hora_formateada) + "|99|||" + str(TotalEmpP) + "|" + str(TotalEmpD) + "|MXN||" + str(TotalEmpP - TotalEmpD) + "|N|01|PUE|04100|\n" )
                archivo.write("EMISOR|CGP911204QU3|INSTITUTO NACIONAL DE LA ECONOMIA SOCIAL|603\n" )
                archivo.write("RECEPTOR|" + str(Persona.RFC) + "|" + str(Nombre_completo) + "|" + "|" + str(CodigoPostal) + "|MEX||605|CN01\n" )
                archivo.write("CONCEPTO|84111505||1|ACT||Pago de nómina|" + str(TotalEmpP) + "|" + str(TotalEmpP) + "|" + str(TotalEmpD) + "|03\n" )
                archivo.write("COMPLEMENTO|Nomina12|O|" + str(FECPAGA) + "|" + str(FECINI) + "|" + str(FECFIN) + "|" + str(DIAS) + "|" + str(TotalEmpP) + "|" + str(TotalEmpD) + "|\n" )
                archivo.write("COMPLEMENTO|Nomina12|EMISOR||0002099093|\n" )
                archivo.write("COMPLEMENTO|Nomina12|RECEPTOR|" + str(Persona.CURP) + "|" + str(CVEISSSTE) + "|" + str(FECALTA) + "|P" + str(PlazaSemana) + "W|02|No|01|02|" + str(Empleado.NumeroEmpleado) + "|" + str(CC) + "|" + str(CPlaza) + "|1|04||" + str(CLABE) + "|" + str(TotalBruto) + "|" + str(TOTALDIARIO) + "|DIF\n" )
            
                # ENCABEZADO PERCEPCIONES
                archivo.write("COMPLEMENTO|Nomina12|PERCEPCIONES|" + str(TotalEmpP) + "|||" + str(TotalEmpP) + "|0.00\n")
            
                CP = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto = "P").all()
                for ConceptoP in CP:
                    Conc = db.session.query(kConcepto).filter_by(idTipoConcepto = "P", idConcepto = ConceptoP.idConcepto).first()
                    
                    PYD = Conc.ClaveSAT # T CONCEPTO PAC
                    CVECONCEPTO = Conc.idConcepto 
                    DesConcepto = Conc.Concepto #DESCRIPCION DEL CONCEPTO

                    if ConceptoP.Porcentaje > 0:
                        IMPORTE =  float((TotalSueldoCG * ConceptoP.Porcentaje) / 100)    
                    else:
                        IMPORTE = ConceptoP.Monto #IMPORTE DE PERCEPCION O DEDUCCION
            
                    # RECORRE TODAS LAS PERCEPCIONES
                    archivo.write("COMPLEMENTO|Nomina12|PERCEPCION|" + str(PYD) + "|P000_" + str(CVECONCEPTO) + "|" + str(DesConcepto) + "|" + str(IMPORTE) + "|0.00\n")
            

                # ENCABEZADO DE DEDUCCIONES
                archivo.write("COMPLEMENTO|Nomina12|DEDUCCIONES|" + str(TotalEmpDD) + "|" + str(TotalEmpDU) + "\n")
                
                CP = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto = "D").all()
                for ConceptoP in CP:
                    Conc = db.session.query(kConcepto).filter_by(idTipoConcepto = "D", idConcepto = ConceptoP.idConcepto).first()
                    
                    PYD = Conc.ClaveSAT # T CONCEPTO PAC
                    CVECONCEPTO = Conc.idConcepto 
                    DesConcepto = Conc.Concepto #DESCRIPCION DEL CONCEPTO

                    if ConceptoP.Porcentaje > 0:
                        if Conc.idConcepto == "50":
                            IMPORTE =  float((TotalSueldoCG * ConceptoP.Porcentaje) / 100) 
                        else:           
                            
                            IMPORTE =  float((TotalBruto * ConceptoP.Porcentaje) / 100)      
                    else:
                        if Conc.idConcepto == "77D":  
                            if NumQuincena == 0:
                                IMPORTE = 7.27
                            else:
                                IMPORTE = 7.28
                        else:
                            IMPORTE = float(ConceptoP.Monto) #IMPORTE DE PERCEPCION O DEDUCCION

                    IMPORTE = "{:.2f}".format(IMPORTE)                    
                    
                    # RECORRE TODAS LAS DEDUCCIONES
                    archivo.write("COMPLEMENTO|Nomina12|DEDUCCION|" + str(PYD) + "|D000_" + str(CVECONCEPTO) + "|" + str(DesConcepto) + "|" + str(IMPORTE) + "\n")





                archivo.write("COMPLEMENTO|Nomina12|OTROSPAGO \n")
                archivo.write("COMPLEMENTO|Nomina12|OTROPAGO|002|S000_SUE|Subsidio al Empleo informativo|0.00 \n")
                archivo.write("COMPLEMENTO|Nomina12|SUBSIDIOALEMPLEO|0.00 \n")
                archivo.write("IMPRESION|TABLA|LEYINAES|ATRIBUTO|" + str(Observaciones) + "| \n")
                archivo.write("TABLA|DEPNOMINA|ATRIBUTO|DescripNomina|" + str(Descripcion) +"\n")
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