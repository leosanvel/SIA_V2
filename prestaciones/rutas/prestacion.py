from .rutas import prestaciones
from flask import render_template

@prestaciones.route('/prestaciones/prestaciones', methods = ['POST', 'GET'])
def pag_prestaciones():
    return render_template('/prestaciones.html', title='Prestaciones')