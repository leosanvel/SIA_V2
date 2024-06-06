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
import os

@nomina.route('/nomina/resumen-nomina', methods = ['POST', 'GET'])
@permisos_de_consulta

def resumen_nomina():
    Nominas = db.session.query(tNomina).filter_by(Estatus=1).all()
    return render_template('/resumen_nomina.html', title='Resumen de la nómina', Nominas=Nominas,)


@nomina.route('/nomina/confirmar_nomina', methods = ['POST', 'GET'])
def confirma_nomina():
    NumNomina = request.form.get("idNomina")
    respuesta = 0

    Nomina = db.session.query(tNomina).filter_by(idNomina=NumNomina,Estatus=1).first()
    if Nomina:
        Nomina.update(Estatus = 2)
        db.session.commit()
        respuesta = 1

    return jsonify({"respuesta":respuesta})

@nomina.route('/nomina/genera_resumen_nomina', methods = ['POST', 'GET'])
@permisos_de_consulta
def generar_resumen():   

    NumNomina = request.form.get("idNomina")
    respuesta = 0
    TotalP = 0
    TotalD = 0
    listaNomina = []
    rutas_archivos = []
    ruta_completa = ""


    Nomina = db.session.query(tNomina).filter_by(idNomina=NumNomina,Estatus=1).first()
    if Nomina:
        numero_quincena = Nomina.Quincena
        mes_pago = Nomina.FechaPago.strftime("%m")
        anio_pago = Nomina.FechaPago.strftime("%Y")
        nombre_carpeta = numero_quincena + mes_pago + anio_pago 
        ruta_completa = "nomina/Doctos/" + nombre_carpeta
        
        if not os.path.exists(ruta_completa):
            os.mkdir(ruta_completa)

        ruta_completa = ruta_completa + "/ResumenNomina.txt"
        
        if os.path.exists(ruta_completa): 
            os.remove(ruta_completa)

        rutas_archivos.append(ruta_completa)            
        with open(ruta_completa, "w") as archivo:
            archivo.write("\t\t\t\tRESUMEN DE LA NOMINA\n" )
            archivo.write("\t\t\t\t"+Nomina.Descripcion+"\n" ) 
            archivo.write ("{:<45}".format("Concepto de Nómina")+"{:<20}".format("No de Registros")+"{:>10}".format("Importe")+"\n")
                    
           
            CConcepto = db.session.query(rNominaPersonas.idTipoConcepto.label("idTipoConcepto"),rNominaPersonas.idConcepto.label("idConcepto"),func.count().label("Empleados"),func.sum(rNominaPersonas.Importe).label("Importe")).filter_by(idNomina=NumNomina).group_by(rNominaPersonas.idConcepto).order_by(rNominaPersonas.idTipoConcepto,rNominaPersonas.idConcepto).all()            
            if CConcepto:
                for CC in CConcepto:
                    NConcepto = db.session.query(kConcepto).filter_by(idTipoConcepto=CC.idTipoConcepto,idConcepto=CC.idConcepto).first()
                    listaNomina.append({"idTipoConcepto":CC.idTipoConcepto,"idConcepto":CC.idConcepto,"Concepto":NConcepto.Concepto,"Empleados":CC.Empleados,"Importe":CC.Importe})        
                    archivo.write ("{:<5}".format(CC.idConcepto)+"{:<40}".format(NConcepto.Concepto)+"{:>10}".format(str(CC.Empleados))+"{:>20}".format(str(CC.Importe))+"\n")
                    if CC.idConcepto != "DT":
                        if CC.Importe > 0:
                            TotalP = TotalP + CC.Importe
                        else:
                            TotalD = TotalD + CC.Importe
                    respuesta = 1
                archivo.write ("{:>75}".format("---------------")+"\n")
                archivo.write ("{:>75}".format(str(TotalP))+"\n")
                archivo.write ("{:>75}".format(str(TotalD))+"\n")
                archivo.write ("{:>75}".format("---------------")+"\n")
                archivo.write ("{:>75}".format(str(TotalP + TotalD))+"\n")

            else:
                respuesta = 0   
    else:
        respuesta = 0
    return jsonify({"respuesta":respuesta,"listanomina":listaNomina,"url_descarga": url_for('nomina.descargar_archivo', nombrecarpeta=nombre_carpeta, nombre_archivo='ResumenNomina.',extencion_archivo='txt'),})


@nomina.route('/descargar_archivo/<nombrecarpeta>/<nombre_archivo>/<extencion_archivo>')
def descargar_archivo(nombrecarpeta,nombre_archivo,extencion_archivo):
    if extencion_archivo == "zip":
        directorio_archivos = os.path.join(current_app.root_path, "nomina", "Doctos", nombrecarpeta, "CFDI")
    else:
        directorio_archivos = os.path.join(current_app.root_path, "nomina", "Doctos", nombrecarpeta)
    return send_from_directory(directory=directorio_archivos, path=nombre_archivo+extencion_archivo, as_attachment=True)