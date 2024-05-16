from flask import Blueprint, render_template, request, session, jsonify, redirect, current_app, send_from_directory, url_for
from flask_login import current_user
from sqlalchemy import or_, inspect, func, and_
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from docx.shared import Cm, Inches, Mm, Emu
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
import pythoncom
import os

from .gestion_empleados import gestion_empleados

@gestion_empleados.route('/rh/gestion-empleados/generar-contratos', methods = ['POST', 'GET'])
def generar_contratoshonorarios():

    return render_template('/generar_contratohonorarios.html', title = 'Generar Contrato de Honorarios')

#Generar Contratos de Honorarios
@gestion_empleados.route("/RH/generarContrato", methods = ['POST'])
def generar_contrato():
    #Abrir documento .docx
    template = DocxTemplate("app/rh/empleado/docs/prueba.docx")
    #Diccionario con la información
    data_contrato = {
        'Nombre': 'Gerardo Alejandro Ruiz Avendaño',
        'Fecha': '12-02-2024'
    }

    # Escribir información en el archivo .docx
    template.render(data_contrato)
    # Guardar documento generado
    template.save(f"app/rh/empleado/docs/Test_1.docx")

    # Convertir archivo .docx a archivo .pdf
    pythoncom.CoInitialize()
    convert("app/rh/empleado/docs/Test_1.docx", "app/rh/empleado/docs/Test_1.pdf")

    return jsonify({"url_descarga": url_for('gestion_empleados.descargar_contrato', nombre_archivo="Test_1.pdf"), "generado": True})

@gestion_empleados.route('/RH/descargar_contrato/<nombre_archivo>')
def descargar_contrato(nombre_archivo):
    directorio_archivos = os.path.join(current_app.root_path, "rh", "empleado", "docs")

    return send_from_directory(directorio_archivos, nombre_archivo, as_attachment=True)