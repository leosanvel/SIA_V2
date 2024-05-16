from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from autenticacion.modelos.modelos import *
from nomina.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import tPersona, rBancoPersona, rSerieNomina, rEmpleado, rEmpleadoPuesto, tPuesto
from rh.gestion_empleados.modelos.domicilio import rDomicilio
from prestaciones.modelos.modelos import rEmpleadoConcepto

import os, zipfile

@nomina.route('/nomina/generar-cfdi', methods = ['POST', 'GET'])
@permisos_de_consulta

def generar_Nomina():
    Quincenas = db.session.query(kQuincena).order_by(kQuincena.idQuincena).all()
    return render_template('/generarNomina.html', title='Generar Nomina',
                           Quincenas = Quincenas,
                           )

@nomina.route('/Nomina/crearCFDI', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_CFDI():
    
    NumNomina = 2
    AnioFiscal = 1
    FechaHoy = datetime.now()

    Nomina = db.session.query(tNomina).filter_by(idNomina = NumNomina,Estatus = 1).first()
    if Nomina:
        strNomina = Nomina.Nomina
        if Nomina.idNomina % 2 == 0:
            QuincenaPar = 0
        else:
            QuincenaPar = 1

    QuincenaPar = 0
    ConsNominaPersonas = db.session.query(rNominaPersonas).filter_by(idNomina = NumNomina).first()
    if ConsNominaPersonas:
        db.session.query(rNominaPersonas).filter_by(idNomina = NumNomina).delete()
        db.session.commit()

    Empleados = db.session.query(rEmpleado).filter_by(idTipoEmpleado = 2,Activo = 1).all()
    for Empleado in Empleados:

###-----Días trabajados

        DiasTrabajados = 15
        DiasDescuento = 0
        DiasGanados = 0

        if Empleado.idPersona == 79:
            DiasDescuento = 14
        else:
            DiasDescuento = 0

        if Empleado.idPersona == 5883:
            DiasGanados = 5
        else:
            DiasGanados = 0

        nuevoregistro = rNominaPersonas(NumNomina,Empleado.idPersona,'','','P','DT',DiasTrabajados + DiasGanados - DiasDescuento)
        db.session.add(nuevoregistro)
        db.session.commit()

        SueldoBruto = 0
        SaldoDiarioBruto = 0
        
        SueldoGravable = 0
        SueldoDiarioGravable = 0
        Sueldo07 = 0
        SueldoCG = 0

### ----Percepción
        EmpleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto = "P").all()
        for EConcepto in EmpleadoConcepto:

            Monto = 0
            MontoDiario = 0
            SueldoDiario07 = 0
            SueldoDiarioCG = 0            

            if EConcepto.idConcepto == "7":
                SueldoGravable = SueldoGravable + EConcepto.Monto                 
                SueldoDiario07 = EConcepto.Monto / 30 
                Monto = SueldoDiario07 * (DiasTrabajados - DiasDescuento)
                Monto = Monto + (SueldoDiario07 * DiasGanados)            
                SueldoBruto = SueldoBruto + (SueldoDiario07 * DiasTrabajados)
                Sueldo07 = Monto
                if Empleado.idPersona == "6735":
                    Monto = 0
                    Sueldo07 = 0
            
            elif EConcepto.idConcepto == "CG":
                SueldoGravable = SueldoGravable + EConcepto.Monto                 
                SueldoDiarioCG = EConcepto.Monto / 30 
                Monto = SueldoDiarioCG * (DiasTrabajados - DiasDescuento)
                Monto = Monto + (SueldoDiarioCG * DiasGanados)
                SueldoCG = Monto
            else:                
                Monto = EConcepto.Monto * 2        
                SueldoGravable = SueldoGravable + Monto        
                MontoDiario = Monto / 30                
                Monto = MontoDiario * (DiasTrabajados - DiasDescuento)
                Monto = Monto + (MontoDiario * DiasGanados)

            if EConcepto.idConcepto == "77" or EConcepto.idConcepto == "A1" or EConcepto.idConcepto == "A2" or EConcepto.idConcepto == "A3" or EConcepto.idConcepto == "A4" or EConcepto.idConcepto == "A5":
                SaldoDiarioBruto = EConcepto.Monto * 2
                SaldoDiarioBruto = SaldoDiarioBruto / 30
                SueldoBruto = SueldoBruto + (SaldoDiarioBruto * DiasTrabajados)
            
            nuevoregistro = rNominaPersonas(NumNomina,EConcepto.idPersona,'','',EConcepto.idTipoConcepto,EConcepto.idConcepto,Monto)
            db.session.add(nuevoregistro)
            db.session.commit()

###         Deducciones
        Monto = 0
        MontoDiario = 0
        EmpleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto = "D").all()
        for EConcepto in EmpleadoConcepto:
            if EConcepto.idConcepto == "77D":  
                if QuincenaPar == 0:
                    Monto = 7.27
                else:
                    Monto = 7.28                
            elif EConcepto.idConcepto == "1":                                               
                CalculoISR = db.session.query(kCalculoISR).filter_by(idAnioFiscal = AnioFiscal).all()
                for ISR in CalculoISR: 
                    if SueldoGravable >= ISR.LimiteInferior and SueldoGravable <= ISR.LimiteSuperior:
                        Monto = SueldoGravable - ISR.LimiteInferior
                        Monto = (Monto * ISR.Porcentaje) / 100
                        Monto = Monto + ISR.CuotaFija
                        MontoDiario = Monto / 30
                        Monto = MontoDiario * (DiasTrabajados - DiasDescuento)
                        Monto = Monto + (MontoDiario * DiasGanados)
            else:
                if EConcepto.Porcentaje > 0:
                    if EConcepto.idConcepto == "50":
                        Monto = (Sueldo07 + SueldoCG) * EConcepto.Porcentaje
                        Monto = Monto / 100
                    else:
                        Monto = (SueldoBruto * EConcepto.Porcentaje) / 100
                else:
                    Monto = EConcepto.Monto
            
            if EConcepto.idConcepto != "1" and EConcepto.idConcepto != "50":
                Monto = round(Monto, 2) * 2
                MontoDiario = round(Monto, 2) / 30
                Monto = MontoDiario * (DiasTrabajados - DiasDescuento)
                Monto = round(Monto, 2) + round(MontoDiario * DiasGanados,2)
                
            Monto = Monto * -1

            nuevoregistro = rNominaPersonas(NumNomina,EConcepto.idPersona,'','',EConcepto.idTipoConcepto,EConcepto.idConcepto,Monto)
            db.session.add(nuevoregistro)
            db.session.commit()

#Genera archivos
    nombre_archivo = nombre_carpeta = str(NumNomina) 
    directorio = "nomina/CFDI/" + nombre_carpeta + "/"
    rutas_archivos = []
    
    if os.path.isfile(directorio + nombre_archivo + ".zip"):
        respuesta = "existente"
    else:
        respuesta = "creado"
        os.makedirs(directorio)
        
        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%dT%H:%M:%S")

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