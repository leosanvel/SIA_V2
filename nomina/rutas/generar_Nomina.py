from flask import render_template, request, jsonify, url_for, current_app, send_from_directory
from flask_login import current_user
from datetime import datetime

from .rutas import nomina
from app import db
from general.herramientas.funciones import *
from catalogos.modelos.modelos import *
from autenticacion.modelos.modelos import *
from nomina.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import rEmpleado
from prestaciones.modelos.modelos import rEmpleadoConcepto, rDiasRetroactivo
from nomina.modelos.modelos import *
from rh.gestion_asistencias.modelos.modelos import rSancionPersona

@nomina.route('/nomina/generar-nomina', methods = ['POST', 'GET'])

def generar_Nomina():
    Nominas = db.session.query(tNomina).filter_by(Estatus=1).all()
    return render_template('/generarNomina.html', title='Generar Nómina',
                           Nominas=Nominas,
                           )
@nomina.route('/Nomina/crearNomina', methods = ['POST', 'GET'])
@permisos_de_consulta
def crear_Nomina():

    NumNomina = request.form.get("idNomina")   
    Observaciones = request.form.get("Observaciones") 
    FechaHoy = datetime.now()
    
    Nomina = db.session.query(tNomina).filter_by(idNomina=NumNomina,Estatus = 1).first()
    if Nomina:
        strNomina = Nomina.Nomina
        AnioFiscal = Nomina.FechaPago.strftime("%Y")
        if Nomina.idNomina % 2 == 0:
            QuincenaPar = 0
        else:
            QuincenaPar = 1

        QuincenaPar = 0
        ConsNominaPersonas = db.session.query(rNominaPersonas).filter_by(idNomina = NumNomina).first()
        if ConsNominaPersonas:
            db.session.query(rNominaPersonas).filter_by(idNomina = NumNomina).delete()
            db.session.commit()
        Empleados = db.session.query(rEmpleado).filter_by(idPersona=2191,idTipoEmpleado = 2,Activo = 1).all()
        #Empleados = db.session.query(rEmpleado).filter_by(idTipoEmpleado = 2,Activo = 1).all()
        for Empleado in Empleados:
    ###-----Días trabajados
            DiasTrabajados = 15
            DiasDescuento = 0
            DiasRetroactivo = 0
            DiasSancion = 0

            DLaborados = db.session.query(rDiasLaborados).filter_by(idNomina=NumNomina,idPersona=Empleado.idPersona).first()
            if DLaborados:
                DiasDescuento = DiasTrabajados - DLaborados.DiasLaborados 
            
            DRetroactivos = db.session.query(rDiasRetroactivo).filter_by(idQuincena=Nomina.idQuincena,idPersona=Empleado.idPersona).first()
            if DRetroactivos:
                DiasRetroactivo = DRetroactivos.Dias                

            nuevoregistro = rNominaPersonas(NumNomina,Empleado.idPersona,'','','P','DT',DiasTrabajados + DiasRetroactivo - DiasDescuento)
            db.session.add(nuevoregistro)
            db.session.commit()

            SueldoBruto = 0
            SaldoDiarioBruto = 0
            
            SueldoGravable = 0
            SueldoAPagar = 0
            Sueldo07 = 0
            SueldoCG = 0

#-----------Percepción
            EmpleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona=Empleado.idPersona,idTipoConcepto="P").all()
            for EConcepto in EmpleadoConcepto:
                Importe = 0
                ImporteDiario = 0
                SueldoDiario07 = 0
                SueldoDiarioCG = 0            

                if EConcepto.idConcepto == "7":
                    SueldoGravable = SueldoGravable + EConcepto.Monto
                    SueldoDiario07 = round(EConcepto.Monto / 30,2)                    
                    SueldoBruto = SueldoBruto + round((EConcepto.Monto / 30) * DiasTrabajados,2)
                    print(str(SueldoBruto))
                    Sueldo07 = round((EConcepto.Monto / 30) * DiasTrabajados,2)                    
                    Importe = round((EConcepto.Monto / 30) * (DiasTrabajados - DiasDescuento),2)
                    if DiasRetroactivo > 0:
                        Importe = Importe + round((EConcepto.Monto / 30) * (DiasRetroactivo),2)                    
                    DSanciones = db.session.query(rSancionPersona).filter_by(idPersona=Empleado.idPersona).all()
                    if DSanciones:
                        for DSancion in DSanciones:
                            MontoSancion = 0
                            if DSancion.FechaInicio >= Nomina.FechaInicial:
                                if DSancion.FechaFin <= Nomina.FechaFinal:
                                    DiasSancion = (DSancion.FechaFin - DSancion.FechaInicio).days + 1                   
                                else:
                                    DiasSancion = (Nomina.FechaFinal - DSancion.FechaInicio).days + 1
                            elif DSancion.FechaFin <= Nomina.FechaFinal:
                                    DiasSancion = (DSancion.FechaFin - Nomina.FechaInicial).days + 1
                        
                            if DiasSancion > 1:
                                MontoSancion = round((EConcepto.Monto / 30) * (DiasSancion),2)
                                MontoSancion = (MontoSancion * DSancion.idPorcentaje) / 100                           
                                Importe = Importe - MontoSancion
                    SueldoAPagar = Importe
                elif EConcepto.idConcepto == "CG":
                    SueldoGravable = SueldoGravable + EConcepto.Monto
                    SueldoCG = round((EConcepto.Monto / 30) * DiasTrabajados,2)                                                            
                    Importe = round((EConcepto.Monto / 30) * (DiasTrabajados - DiasDescuento),2)
                    if DiasRetroactivo > 0:
                        Importe = Importe + round((EConcepto.Monto / 30) * (DiasRetroactivo),2)
                else:
                    Importe = EConcepto.Monto * 2        
                    SueldoGravable = SueldoGravable + Importe        
                    Importe = round(((EConcepto.Monto*2) / 30) * (DiasTrabajados - DiasDescuento),2)
                    if DiasRetroactivo > 0:
                        Importe = Importe + round(((EConcepto.Monto*2) / 30) * (DiasRetroactivo),2)

                if EConcepto.idConcepto == "77" or EConcepto.idConcepto == "A1" or EConcepto.idConcepto == "A2" or EConcepto.idConcepto == "A3" or EConcepto.idConcepto == "A4" or EConcepto.idConcepto == "A5":
                    SueldoBruto = SueldoBruto + EConcepto.Monto
                    print(str(SueldoBruto))
                    
                nuevoregistro = rNominaPersonas(NumNomina,EConcepto.idPersona,'','',EConcepto.idTipoConcepto,EConcepto.idConcepto,Importe)
                db.session.add(nuevoregistro)
                db.session.commit()
#-----------Deducciones                
            Importe = 0
            ImporteADescontar = 0
            MontoDiarioDeduccion = 0
            EmpleadoConcepto = db.session.query(rEmpleadoConcepto).filter_by(idPersona = Empleado.idPersona, idTipoConcepto = "D").all()
            for EConcepto in EmpleadoConcepto:
                if EConcepto.idConcepto == "77D":  
                    if QuincenaPar == 0:
                        ImporteADescontar = 7.27
                    else:
                        ImporteADescontar = 7.28                
                
                elif EConcepto.idConcepto == "1":                                               
                    CalculoISR = db.session.query(kCalculoISR).filter_by(idAnioFiscal = AnioFiscal).all()
                    for ISR in CalculoISR: 
                        if SueldoGravable >= ISR.LimiteInferior and SueldoGravable <= ISR.LimiteSuperior:
                            Importe = SueldoGravable - ISR.LimiteInferior
                            Importe = (Importe * ISR.Porcentaje) / 100
                            Importe = Importe + ISR.CuotaFija
                            ImporteADescontar = Importe

                            Importe = round((ImporteADescontar / 30) * (DiasTrabajados - DiasDescuento),2)
                            if DiasRetroactivo > 0:
                                Importe = Importe + round((ImporteADescontar / 30) * (DiasRetroactivo),2)
                elif EConcepto.idConcepto == "50":
                    ImporteADescontar = round(((Sueldo07 + SueldoCG) * EConcepto.Porcentaje) / 100,2)
                else:
                    if EConcepto.Porcentaje > 0:                        
                        ImporteADescontar = round((SueldoBruto * EConcepto.Porcentaje) / 100,2)         
                        print("Concepto: ",str(EConcepto.idConcepto)," - sueldo bruto: ", str(SueldoBruto),"- Porcentaje: ",str(EConcepto.Porcentaje),"- Importe: ",str(ImporteADescontar))                   
                    else:
                        ImporteADescontar = EConcepto.Monto
                
                CalcularMonto = 0
                if EConcepto.idConcepto != "1":
                    #print("Concepto: ",str(EConcepto.idConcepto)," - sueldo bruto: ", str(SueldoAPagar))
                    if SueldoAPagar > 0:
                        CalcularMonto = 1
                    else:
                        Importe = 0
                
                if CalcularMonto == 1:                    
                    Importe = round(((ImporteADescontar * 2) / 30) * (DiasTrabajados - DiasDescuento),2)
                    if DiasRetroactivo > 0:
                        Importe = Importe + round(((ImporteADescontar*2) / 30) * (DiasRetroactivo),2)

                Importe = Importe * -1
                print(str(Importe))
                nuevoregistro = rNominaPersonas(NumNomina,EConcepto.idPersona,'','',EConcepto.idTipoConcepto,EConcepto.idConcepto,Importe)
                db.session.add(nuevoregistro)
                db.session.commit()

                #print(str(Empleado.NumeroEmpleado))

            Nomina.update(Observaciones = Observaciones)        
            respuesta = "1"
        else:
            respuesta = "0"
    
    return jsonify({"respuesta":respuesta})