from datetime import datetime
from sqlalchemy import func
from app import db
#from rh.gestion_empleado.modelos.empleado import Puesto

class kCentroCostos(db.Model):
    __tablename__ = "kcentrocosto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idCentroCosto = db.Column(db.Integer, primary_key = True)
    Clave = db.Column(db.Integer, nullable = True)
    CentroCosto = db.Column(db.String(50), nullable = True)
    idEntidad = db.Column(db.String(2), nullable = True)
    Materia = db.Column(db.String(25), nullable = True)
    Abreviatura = db.Column(db.String(25), nullable = True)
    idNivelRegistroContable = db.Column(db.String(2), nullable = True)
    idCiudad = db.Column(db.Integer, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "CentroCostos", cascade = "all, delete-orphan")

    def __init__(self, idCentroCosto, Clave, CentroCosto, idEntidad, Materia, Abreviatura, idNivelRegistroContable, idCiudad):
        self.idCentroCosto = idCentroCosto
        self.Clave = Clave
        self.CentroCosto = CentroCosto
        self.idEntidad = idEntidad
        self.Materia = Materia
        self.Abreviatura = Abreviatura
        self.idNivelRegistroContable = idNivelRegistroContable
        self.idCiudad = idCiudad

class kGrado(db.Model):
    __tablename__ = "kgrado"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}
    
    idGrado = db.Column(db.Integer, primary_key = True)
    Grado = db.Column(db. String(50), nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "Grado", cascade = "all, delete-orphan")

    def __init__(self, idGrado, Grado):
        self.idGrado = idGrado
        self.Grado = Grado

class kCaracterOcupacional(db.Model):
    __tablename__ = "kcaracterocupacional"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idCaracterOcupacional = db.Column(db.Integer, primary_key = True)
    CaracterOcupacional = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "CaracterOcupacional", cascade = "all, delete-orphan")

    def __init__(self, idCaracterOcupacional, CaracterOcupacional, Activo):
        self.idCaracterOcupacional = idCaracterOcupacional
        self.CaracterOcupacional = CaracterOcupacional
        self.Activo = Activo

class kNivel(db.Model):
    __tablename__ = "knivel"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNivel = db.Column(db.Integer, primary_key = True)
    Nivel = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "Nivel", cascade = "all, delete-orphan")

    def __init__(self, idNivel, Nivel, Activo):
        self.idNivel = idNivel
        self.Nivel = Nivel
        self.Activo = Activo

class kGrupo(db.Model):
    __tablename__ = "kgrupo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idGrupo = db.Column(db.Integer, primary_key = True)
    idTipoAlta = db.Column(db.Integer, nullable = True)
    Grupo = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)
    idEsquemaHonorarios = db.Column(db.Integer, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "Grupo", cascade = "all, delete-orphan")

    def __init__(self, idGrupo, idTipoAlta, Grupo, Activo, idEsquemaHonorarios):
        self.idGrupo = idGrupo
        self.idTipoAlta = idTipoAlta
        self.Grupo = Grupo
        self.Activo = Activo
        self.idEsquemaHonorarios = idEsquemaHonorarios

class kZonaEconomica(db.Model):
    __tablename__ = "kzonaeconomica"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idZonaEconomica = db.Column(db.Integer, primary_key = True)
    ZonaEconomica = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "ZonaEconomica", cascade = "all, delete-orphan")

    def __init__(self, idZonaEconomica, ZonaEconomica, Activo):
        self.idZonaEconomica = idZonaEconomica
        self.ZonaEconomica = ZonaEconomica
        self.Activo = Activo

class kRamo(db.Model):
    __tablename__ = "kramo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idRamo = db.Column(db.Integer, primary_key = True)
    Ramo = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    UAs = db.relationship("kUA", back_populates = "Ramo", cascade = "all, delete-orphan")

    def __init__(self, idRamo, Ramo, Activo):
        self.idRamo = idRamo
        self.Ramo = Ramo
        self.Activo = Activo

class kUA(db.Model):
    __tablename__ = "kua"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idRamo = db.Column(db.Integer, db.ForeignKey(kRamo.idRamo), nullable = True)
    idUA = db.Column(db.Integer, primary_key = True)
    UA = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    #Relación
    Ramo = db.relationship('kRamo', back_populates = "UAs", uselist = False, single_parent = True)
    Puestos = db.relationship('tPuesto', back_populates = "UA", cascade = "all, delete-orphan")

    def __init__(self, idRamo, idUA, UA, Activo):
        self.idRamo = idRamo
        self.idUA = idUA
        self.UA = UA
        self.Activo = Activo

class kEstatusPuesto(db.Model):
    __tablename__ = "kestatuspuesto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEstatusPuesto = db.Column(db.Integer, primary_key = True)
    EstatusPuesto = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "EstatusPuesto", cascade = "all, delete-orphan")

    def __init__(self, idEstatusPuesto, EstatusPuesto, Activo):
        self.idEstatusPuesto = idEstatusPuesto
        self.EstatusPuesto = EstatusPuesto
        self.Activo = Activo

class kCentroTrabajo(db.Model):
    __tablename__ = "kcentrotrabajo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idCentroTrabajo = db.Column(db.Integer, primary_key = True)
    CentroTrabajo = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)
    
    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "CentroTrabajo", cascade = "all, delete-orphan")

    def __init__(self, idCentroTrabajo, CentroTrabajo, Activo):
        self.idCentroTrabajo = idCentroTrabajo
        self.CentroTrabajo = CentroTrabajo
        self.Activo = Activo

class kTipoPlazaPuesto(db.Model):
    __tablename__ = "ktipoplaza"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoPlazaPuesto = db.Column(db.Integer, primary_key = True)
    TipoPlazaPuesto = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('tPuesto', back_populates = "TipoPlazaPuesto", cascade = "all, delete-orphan")

    def __init__(self, idTipoPlazaPuesto, TipoPlazaPuesto, Activo):
        self.idTipoPlazaPuesto = idTipoPlazaPuesto
        self.TipoPlazaPuesto = TipoPlazaPuesto
        self.Activo = Activo

class kVigencia(db.Model):
    __tablename__ = "kvigencia"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idVigencia = db.Column(db.Integer, primary_key = True)
    Vigencia = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    #Relación
    Puestos = db.relationship('tPuesto', back_populates = "Vigencia", cascade = "all, delete-orphan")

    def __init__(self, idVigencia, Vigencia, Activo):
        self.idVigencia = idVigencia
        self.Vigencia = Vigencia
        self.Activo = Activo

#
class kTipoPersona(db.Model):
    __tablename__ = "ktipopersona"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoPersona = db.Column(db.Integer, primary_key = True)
    TipoPersona = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relacion
    Personas = db.relationship("tPersona", back_populates = "TipoPersona", cascade = "all, delete-orphan")

    def __init__(self, idTipoPersona, TipoPersona, Activo):
        self.idTipoPersona = idTipoPersona
        self.TipoPersona = TipoPersona
        self.Activo = Activo

# 
class kNacionalidad(db.Model):
    __tablename__ = "knacionalidad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNacionalidad = db.Column(db.Integer, primary_key = True)
    Nacionalidad = db.Column(db.String(50), nullable = True)
    idNacionalidadFP = db.Column(db.String(5), nullable = True)
    idPaisFP = db.Column(db.String(10), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idNacionalidad, Nacionalidad, idNacionalidadFP, idPaisFP, Activo):
        self.idNacionalidad = idNacionalidad
        self.Nacionalidad = Nacionalidad
        self.idNacionalidadFP = idNacionalidadFP
        self.idPaisFP = idPaisFP
        self.Activo = Activo

class kEstadoCivil(db.Model):
    __tablename__ = "kestadocivil"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEstadoCivil = db.Column(db.Integer, primary_key = True)
    EstadoCivil = db.Column(db.String(30), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idEstadoCivil, EstadoCivil, Activo):
        self.idEstadoCivil = EstadoCivil
        self.EstadoCivil = EstadoCivil
        self. Activo = Activo

class kTipoEmpleado(db.Model):
    __tablename__ = "ktipoempleado"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    TipoEmpleado = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoEmpleado, TipoEmpleado, Activo):
        self.idTipoEmpleado = idTipoEmpleado
        self.TipoEmpleado = TipoEmpleado
        self.Activo = Activo

class kTipoAlta(db.Model):
    __tablename__ = "ktipoalta"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoAlta = db.Column(db.Integer, primary_key = True)
    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    TipoAlta = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoAlta, idTipoEmpleado, TipoAlta, Activo):
        self.idTipoAlta = idTipoAlta
        self.idTipoEmpleado = idTipoEmpleado
        self.TipoAlta = TipoAlta
        self.Activo = Activo

class kQuincena(db.Model):
    __tablename__ = "kquincena"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idQuincena = db.Column(db.Integer, primary_key = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    Descripcion = db.Column(db.String(50), nullable = True)

    def __init__(self, idQuincena, FechaInicio, FechaFin, Descripcion):
        self.idQuincena = idQuincena
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.Descripcion = Descripcion

class kEscolaridad(db.Model):
    __tablename__ = "kescolaridad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEscolaridad = db.Column(db.Integer, primary_key = True)
    Escolaridad = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idEscolaridad, Escolaridad, Activo):
        self.idEscolaridad = idEscolaridad
        self.Escolaridad = Escolaridad
        self.Activo = Activo

class rEscolaridadNivel(db.Model):
    __tablename__ = "rescolaridadnivel"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEscolaridad = db.Column(db.Integer, primary_key = True)
    idNivelEscolaridad = db.Column(db.Integer, primary_key = True)

    def __init__(self, idEscolaridad, idNivelEscolaridad):
        self.idEscolaridad = idEscolaridad
        self.idNivelEscolaridad = idNivelEscolaridad

class kNivelEscolaridad(db.Model):
    __tablename__ = "knivelescolaridad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNivelEscolaridad = db.Column(db.Integer, primary_key = True)
    NivelEscolaridad = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idNivelEscolaridad, NivelEscolaridad, Activo):
        self.idNivelEscolaridad = idNivelEscolaridad
        self.NivelEscolaridad = NivelEscolaridad

class kInstitucionEscolar(db.Model):
    __tablename__ = "kinstitucionescolar"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idInstitucionEscolar = db.Column(db.Integer, primary_key = True)
    InstitucionEscolar = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idInstitucionEscolar, InstitucionEscolar, Activo):
        self.idInstitucionEscolar = idInstitucionEscolar
        self.InstitucionEscolar = InstitucionEscolar
        self.Activo = Activo

class rEscolaridadInstitucion(db.Model):
    __tablename__ = "rescolaridadinstitucion"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEscolaridad = db.Column(db.Integer, primary_key = True)
    idInstitucionEscolar = db.Column(db.Integer, primary_key = True)

    def __init__(self, idEscolaridad, idInstitucionEscolar):
        self.idEscolaridad = idEscolaridad
        self.idInstitucionEscolar - idInstitucionEscolar

class kFormacionEducativa(db.Model):
    __tablename__ = "kformacioneducativa"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idFormacionEducativa = db.Column(db.Integer, primary_key = True)
    FormacionEducativa = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idFormacionEducativa, FormacionEducativa, Activo):
        self.idFormacionEducativa = idFormacionEducativa
        self.FormacionEducativa = FormacionEducativa
        self.Activo = Activo

class rInstitucionFormacion(db.Model):
    __tablename__ = "rinstitucionformacion"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idInstitucionEscolar = db.Column(db.Integer, primary_key = True)
    idFormacionEducativa = db.Column(db.Integer, primary_key = True)

    def __init__(self, idInstitucionEscolar, idFormacionEducativa):
        self.idInstitucionEscolar = idInstitucionEscolar
        self.idFormacionEducativa = idFormacionEducativa

class kEntidad(db.Model):
    __tablename__ = "kentidad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEntidad = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Entidad = db.Column(db.String(50), nullable = True)
    Abreviatura = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idEntidad, Consecutivo, Entidad, Abreviatura, Activo):
        self.idEntidad = idEntidad
        self.Consecutivo = Consecutivo
        self.Entidad = Entidad
        self.Abreviatura = Abreviatura
        self. Activo = Activo

class kMunicipio(db.Model):
    __tablename__ = "kmunicipio"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEntidad = db.Column(db.Integer, primary_key = True)
    idMunicipio = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Municipio = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idEntidad, idMunicipio, Consecutivo, Municipio, Activo):
        self.idEntidad = idEntidad
        self.idMunicipio = idMunicipio
        self.Consecutivo = Consecutivo
        self.Municipio = Municipio
        self.Activo = Activo

class kLocalidad(db.Model):
    __tablename__ = "klocalidad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idEntidad = db.Column(db.Integer, primary_key = True)
    idMunicipio = db.Column(db.Integer, primary_key = True)
    idLocalidad = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Localidad = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idEntidad, idMunicipio, idLocalidad, Consecutivo, Localidad, Activo):
        self.idEntidad = idEntidad
        self.idMunicipio = idMunicipio
        self.idLocalidad = idLocalidad
        self.Consecutivo = Consecutivo
        self.Localidad = Localidad
        self.Activo = Activo

class kTipoAsentamiento(db.Model):
    __tablename__ = "ktipoasentamiento"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoAsentamiento = db.Column(db.Integer, primary_key = True)
    TipoAsentamiento = db.Column(db.String(45), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoAsentamiento, TipoAsentamiento, Activo):
        self.idTipoAsentamiento = idTipoAsentamiento
        self.TipoAsentamiento = TipoAsentamiento
        self.Activo = Activo

class kVialidad(db.Model):
    __tablename__ = "kvialidad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idVialidad = db.Column(db.Integer, primary_key = True)
    Vialidad = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idVialidad, Vialidad, Activo):
        self. idVialidad = idVialidad
        self.Vialidad = Vialidad
        self.Activo = Activo

class kCodigoPostal(db.Model):
    __tablename__ = "kcodigopostal"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    CodigoPostal = db.Column(db.Integer, primary_key = True)
    idEntidad = db.Column(db.Integer, primary_key = True)
    idMunicipio = db.Column(db.Integer, primary_key = True)
    idTipoAsentamiento = db.Column(db.Integer, primary_key = True)
    idAsentamiento = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Asentamiento = db.Column(db.String(250), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, CodigoPostal, idEntidad, idMunicipio, idTipoAsentamiento, idAsentamiento, Consecutivo, Asentamiento, Activo):
        self.CodigoPostal = CodigoPostal
        self.idEntidad = idEntidad
        self.idMunicipio = idMunicipio
        self.idTipoAsentamiento = idTipoAsentamiento
        self.idAsentamiento = idAsentamiento
        self.Consecutivo = Consecutivo
        self.Asentamiento = Asentamiento
        self.Activo = Activo

class Plazas(db.Model):
    __tablename__ = "kPlaza"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPlaza = db.Column(db.String(15), primary_key = True)
    Plaza =  db.Column(db.String(250), nullable = True)

    def __init__(self, idPlaza, Plaza):
        self.idPlaza = idPlaza
        self.Plaza = Plaza

class kConcepto(db.Model):
    __tablename__ = "kconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    Concepto = db.Column(db.String(250), nullable = False)
    Abreviatura = db.Column(db.String(25), nullable = False)
    Porcentaje = db.Column(db.Numeric(11, 3), nullable = True)
    Monto = db.Column(db.Numeric(11, 2), nullable = True)
    ClaveSAT = db.Column(db.String(25), nullable = False)
    idTipoPago = db.Column(db.Integer, nullable = False)
    Activo = db.Column(db.Integer, nullable = False)


    def __init__(self,idTipoConcepto, idConcepto, Concepto, Abreviatura, Porcentaje, Monto, ClaveSAT, idTipoPago, Activo):
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Concepto = Concepto
        self.Abreviatura = Abreviatura
        self.Porcentaje = Porcentaje
        self.Monto = Monto
        self.ClaveSAT = ClaveSAT
        self.idTipoPago = idTipoPago
        self.Activo = Activo

class kTipoConcepto(db.Model):
    __tablename__ = "ktipoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    TipoConcepto = db.Column(db.String(25), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idTipoConcepto, TipoConcepto, Activo):
        self.idTipoConcepto = idTipoConcepto
        self.TipoConcepto = TipoConcepto
        self.Activo = Activo

class kTipoPago(db.Model):
    __tablename__ = "ktipopago"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoPago = db.Column(db.String(1), primary_key = True)
    TipoPago = db.Column(db.String(25), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idTipoPago, TipoPago, Activo):
        self.idTipoPago = idTipoPago
        self.TipoPago = TipoPago
        self.Activo = Activo

class kCausaBaja(db.Model):
    __tablename__ = "kcausabaja"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    idCausaBaja = db.Column(db.Integer, primary_key = True)
    CausaBaja = db.Column(db.String(300))
    Activo = db.Column(db.Integer)

    def __init__(self, idTipoEmpleado, idCausaBaja, CausaBaja, Activo):
        self.idTipoEmpleado = idTipoEmpleado
        self.idCausaoBaja = idCausaBaja
        self.CausaBaja = CausaBaja
        self.Activo = Activo

class kBancos(db.Model):
    __tablename__ = "kbancos"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idBanco = db.Column(db.Integer, primary_key = True)
    Codigo = db.Column(db.String(3), nullable = True)
    Clave = db.Column(db.String(5), nullable = True)
    Nombre = db.Column(db.String(50), nullable = True)

    def __init__(self, idBanco, Codigo, Clave, Nombre):
        self.idBanco = idBanco
        self.Codigo = Codigo
        self.Clave = Clave
        self.Nombre = Nombre