from .gestion_empleados import gestion_empleados

from flask import Blueprint, request, session

# from catalogos.modelos.modelos import *
from rh.gestion_empleados.modelos.empleado import *
from app import db

# INFO EMPLEADO
@gestion_empleados.route('/select_TipAlt', methods = ['POST'])
def select_TipAlt():
    TipEmpl = request.form.get('idTipoEmpleo')
    ret = '<option value="0">-- Seleccione --</option>'
    TipAlts = db.session.query(kTipoAlta).filter_by(idTipoEmpleado=TipEmpl, Activo = 1).all()
    for entry in TipAlts:
        ret += '<option value="{}">{}</option>'.format(entry.idTipoAlta, entry.TipoAlta)
    return ret

@gestion_empleados.route('/select_Grupo', methods=['POST'])
def select_Grupo():
    TipAlt = request.form.get('idTipoAlta')
    ret = '<option value="0">-- Seleccione --</option>'
    Grupos = db.session.query(kGrupo).filter_by(idTipoAlta=TipAlt, Activo = 1).all()
    for entry in Grupos:
        ret += '<option value="{}">{}</option>'.format(entry.idGrupo, entry.Grupo)
    return ret

# DOMICILIOS
@gestion_empleados.route('/select_municipio', methods = ['POST'])
def select_municipio():
    Entidad = request.form.get('Entidad')
    ret = '<option value="0">-- Seleccione --</option>'
    municipios = db.session.query(kMunicipio).filter_by(idEntidad = Entidad, Activo = 1).all()
    for entry in municipios:
        ret += '<option value="{}">{}</option>'.format(entry.idMunicipio, entry.Municipio)
    return ret

@gestion_empleados.route('/select_localidad', methods = ['POST'])
def select_localidad():
    Entidad = request.form.get('Entidad')
    Municipio = request.form.get('Municipio')
    ret = '<option value="0">-- Seleccione --</option>'
    localidades = db.session.query(kLocalidad).filter_by(idEntidad = Entidad, idMunicipio = Municipio, Activo = 1).order_by(kLocalidad.Localidad).all()
    for entry in localidades:
        ret += '<option value="{}">{}</option>'.format(entry.idLocalidad, entry.Localidad)
    return ret

@gestion_empleados.route('/select_asentamiento', methods = ['POST'])
def select_asentamiento():
    Entidad = request.form.get('Entidad')
    Municipio = request.form.get('Municipio')
    TipoAsentamiento = request.form.get('TipoAsentamiento')
    ret = '<option value="0">-- Seleccione --</option>'
    Asentamientos = db.session.query(kCodigoPostal).filter_by(idEntidad = Entidad, idMunicipio = Municipio, idTipoAsentamiento = TipoAsentamiento, Activo = 1).all()
    for entry in Asentamientos:
        ret += '<option value="{}">{}</option>'.format(entry.idAsentamiento, entry.Asentamiento)
    return ret

@gestion_empleados.route('/cargar_Plaza', methods = ['POST'])
def cargar_Plaza():
    idCentroCosto = request.form.get('idCentroCostos')
    ret = '<option value="0">-- Seleccione --</option>'
    Plazas = db.session.query(tPuesto).filter_by(idCentroCosto = idCentroCosto, idEstatusPuesto = 2).all()
    for entry in Plazas:
        ret += '<option value="{}">{}</option>'.format(entry.ConsecutivoPuesto, entry.Puesto)
    return ret

@gestion_empleados.route("/cargar-puestos-honorarios", methods = ['POST'])
def cargar_puestos_honorarios():
    ret = '<option value="0">-- Seleccione --</option>'
    Puestos_honorarios = db.session.query(tPuestoHonorarios).filter_by(Activo = 1).order_by(tPuestoHonorarios.PuestoHonorarios).all()
    for entry in Puestos_honorarios:
        ret += '<option value="{}">{}</option>'.format(entry.idPuestoHonorarios, entry.PuestoHonorarios)
    return ret

@gestion_empleados.route('/cargar_EstNivEsc', methods = ['POST'])
def cargar_EstNivEsc():
    NivEsc = request.form.get('idEscolaridad')
    ret = '<option value="0">-- Seleccione --</option>'
    NivEscs = db.session.query(kNivelEscolaridad).outerjoin(rEscolaridadNivel, kNivelEscolaridad.idNivelEscolaridad == rEscolaridadNivel.idNivelEscolaridad).filter(rEscolaridadNivel.idEscolaridad == NivEsc, kNivelEscolaridad.Activo == 1).order_by(kNivelEscolaridad.NivelEscolaridad).all()
    for entry in NivEscs:
        ret += '<option value="{}">{}</option>'.format(entry.idNivelEscolaridad, entry.NivelEscolaridad)
    return ret

@gestion_empleados.route('/cargar_Escuela', methods = ['POST'])
def cargar_Escuela():
    NivEscolar = request.form.get('idEscolaridad')
    ret = '<option value="0">-- Seleccione --</option>'
    Escuelas = db.session.query(kInstitucionEscolar).outerjoin(rEscolaridadInstitucion, kInstitucionEscolar.idInstitucionEscolar == rEscolaridadInstitucion.idInstitucionEscolar).filter(rEscolaridadInstitucion.idEscolaridad == NivEscolar, kInstitucionEscolar.Activo == 1).order_by(kInstitucionEscolar.InstitucionEscolar).all()
    for entry in Escuelas:
        ret += '<option value="{}">{}</option>'.format(entry.idInstitucionEscolar, entry.InstitucionEscolar)
    return ret

@gestion_empleados.route('/cargar_FormacionEducativa', methods = ['POST'])
def cargar_Formacion_Educativa():
    institucionEscolar = request.form.get('idInstitucionEscolar')
    ret = '<option value="0">-- Seleccione --</option>'
    formaciones = db.session.query(kFormacionEducativa).outerjoin(rInstitucionFormacion, kFormacionEducativa.idFormacionEducativa == rInstitucionFormacion.idFormacionEducativa).filter(rInstitucionFormacion.idInstitucionEscolar == institucionEscolar, kFormacionEducativa.Activo == 1).order_by(kFormacionEducativa.FormacionEducativa).all()
    for entry in formaciones:
        ret += '<option value="{}">{}</option>'.format(entry.idFormacionEducativa, entry.FormacionEducativa)
    return ret

@gestion_empleados.route("/rh/gestion-empleados/obtener-nacionalidad", methods = ["POST"])
def cargar_Nacionalidad():
    Nacionalidad = request.form.get("Nacionalidad")
    ret = '<option value="0">-- Seleccione --</option>'
    Nacionalidades = db.session.query(kNacionalidad).filter_by(Activo = 1).order_by(kNacionalidad.Nacionalidad).all()
    for entry in Nacionalidades:
        if entry.Nacionalidad == Nacionalidad:
            ret += '<option selected="true" value="{}">{}</option>'.format(entry.idNacionalidad, entry.Nacionalidad)
        else:
            ret += '<option value="{}">{}</option>'.format(entry.idNacionalidad, entry.Nacionalidad)
    return ret

@gestion_empleados.route("/rh/gestion-empleados/obtener-formacion-educativa", methods = ["POST"])
def cargar_FormacionEducativa():
    FormacionEducativa = request.form.get("FormacionEducativa")
    ret = '<option value="0">-- Seleccione --</option>'
    FormacionesEducativas = db.session.query(kFormacionEducativa).filter_by(Activo = 1).order_by(kFormacionEducativa.FormacionEducativa).all()
    for entry in FormacionesEducativas:
        if entry.FormacionEducativa == FormacionEducativa:
            ret += '<option selected="true" value="{}">{}</option>'.format(entry.idFormacionEducativa, entry.FormacionEducativa)
        else:
            ret += '<option value="{}">{}</option>'.format(entry.idFormacionEducativa, entry.FormacionEducativa)

    return ret

@gestion_empleados.route("/rh/gestion-empleados/obtener-institucion-escolar", methods = ["POST"])
def cargar_InstitucionEscolar():
    InstitucionEscolar = request.form.get("InstitucionEscolar")
    ret = '<option value="0">-- Seleccione --</option>'
    InstitucionesEscolares = db.session.query(kInstitucionEscolar).filter_by(Activo = 1).order_by(kInstitucionEscolar.InstitucionEscolar).all()
    for entry in InstitucionesEscolares:
        if entry.InstitucionEscolar == InstitucionEscolar:
            ret += '<option selected="true" value="{}">{}</option>'.format(entry.idInstitucionEscolar, entry.InstitucionEscolar)
        else:
            ret += '<option value="{}">{}</option>'.format(entry.idInstitucionEscolar, entry.InstitucionEscolar)

    return ret

@gestion_empleados.route("/rh/gestion-empleados/obtener-idiomas", methods = ["POST"])
def obtener_idiomas():
    ret = '<option value="0">-- Seleccione --</option>'

    Idiomas = db.session.query(kIdiomas).filter_by(Activo = 1).order_by(kIdiomas.Idioma).all()

    for entry in Idiomas:
        ret += '<option value="{}">{}</option>'.format(entry.idIdioma, entry.Idioma)

    return ret

@gestion_empleados.route("/rh/gestion-empleados/obtener-lenguas-indigenas", methods = ["POST"])
def obtener_lenguas_indigenas():
    LenguaIndigena = request.form.get("LenguaIndigena")
    ret = '<option value="0">-- Seleccione --</option>'

    LenguasIndigenas = db.session.query(kLenguasIndigenas).filter_by(Activo = 1).order_by(kLenguasIndigenas.LenguaIndigena).all()

    for entry in LenguasIndigenas:
        if entry.LenguaIndigena == LenguaIndigena:
            ret += '<option selected="true" value="{}">{}</option>'.format(entry.idLenguaIndigena, entry.LenguaIndigena)
        else:
            ret += '<option value="{}">{}</option>'.format(entry.idLenguaIndigena, entry.LenguaIndigena)
    
    return ret