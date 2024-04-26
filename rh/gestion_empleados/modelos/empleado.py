from app import db
from catalogos.modelos.modelos import *

class tPersona(db.Model):
    __tablename__ = "tpersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    CURP = db.Column(db.String(18), nullable = True)
    Nombre = db.Column(db.String(50), nullable = True)
    ApPaterno = db.Column(db.String(50), nullable = True)
    ApMaterno = db.Column(db.String(50), nullable = True)
    Sexo = db.Column(db.String(20), nullable = True)
    FechaNacimiento = db.Column(db.Date, nullable = True)
    RFC = db.Column(db.String(13), nullable = True)
    idNacionalidad = db.Column(db.Integer, nullable = True)
    CalidadMigratoria = db.Column(db.String(100), nullable = True)
    TelCasa = db.Column(db.String(10), nullable = True)
    TelCelular = db.Column(db.String(10), nullable = True)
    idTipoPersona = db.Column(db.Integer, db.ForeignKey(kTipoPersona.idTipoPersona), nullable = True)
    idEstadoCivil = db.Column(db.Integer, nullable = True)
    CorreoPersonal = db.Column(db.String(150), nullable = True)

    # Relaciones
    TipoPersona = db.relationship("kTipoPersona", back_populates = "Personas", uselist = False, single_parent = True)
    Empleado = db.relationship("rEmpleado", uselist = False, back_populates = "Persona", cascade = "all, delete-orphan", single_parent = True)

    def __init__(self, idPersona, CURP, Nombre, ApPaterno, ApMaterno, Sexo, FechaNacimiento, RFC, idNacionalidad,
                 CalidadMigratoria, TelCasa, TelCelular, idTipoPersona, idEstadoCivil, CorreoPersonal):
        self.idPersona = idPersona
        self.CURP = CURP
        self.Nombre = Nombre
        self.ApPaterno = ApPaterno
        self.ApMaterno = ApMaterno
        self.Sexo = Sexo
        self.FechaNacimiento = FechaNacimiento
        self.RFC = RFC
        self.idNacionalidad = idNacionalidad
        self.CalidadMigratoria = CalidadMigratoria
        self.TelCasa = TelCasa
        self.TelCelular = TelCelular
        self.idTipoPersona = idTipoPersona
        self.idEstadoCivil = idEstadoCivil
        self.CorreoPersonal = CorreoPersonal
class tPuesto(db.Model):
    __tablename__ = "tpuesto"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    # idRamo = db.Column(db.Integer, nullable = True)
    idUA = db.Column(db.Integer, db.ForeignKey(kUA.idUA), nullable = True)
    ConsecutivoPuesto = db.Column(db.Integer, primary_key = True)
    CodigoPuesto = db.Column(db.String(50), nullable = True)
    Puesto = db.Column(db.String(150), nullable = True)
    idZonaEconomica = db.Column(db.Integer, db.ForeignKey(kZonaEconomica.idZonaEconomica), nullable = True)
    ReferenciaTabular = db.Column(db.String(10), nullable = True)
    ConsPuesto = db.Column(db.Integer, nullable = True)    
    idTipoPlazaPuesto = db.Column(db.Integer, db.ForeignKey(kTipoPlazaPuesto.idTipoPlazaPuesto), nullable = True)
    idCaracterOcupacional = db.Column(db.Integer, db.ForeignKey(kCaracterOcupacional.idCaracterOcupacional), nullable = True)
    idTipoFuncion = db.Column(db.Integer, nullable = True)
    NivelSalarial = db.Column(db.String(5), nullable = True)
    Tabulador = db.Column(db.Integer, nullable = True)
    CodigoPresupuestal = db.Column(db.String(10), nullable = True)
    OrdinalCP = db.Column(db.Integer, nullable = True)
    idGrupo = db.Column(db.Integer, db.ForeignKey(kGrupo.idGrupo), nullable = True)
    idGrado = db.Column(db.Integer, db.ForeignKey(kGrado.idGrado), nullable = True)
    idNivel = db.Column(db.Integer, db.ForeignKey(kNivel.idNivel), nullable = True)
    idEstatusPuesto = db.Column(db.Integer, db.ForeignKey(kEstatusPuesto.idEstatusPuesto), nullable = True)
    idVigencia = db.Column(db.Integer, db.ForeignKey(kVigencia.idVigencia), nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    idCentroTrabajo = db.Column(db.Integer, db.ForeignKey(kCentroTrabajo.idCentroTrabajo), nullable = True)
    FolioSival = db.Column(db.String(15), nullable = True)
    RegimenLaboral = db.Column(db.String(15), nullable = True)
    RemuneracionTotal = db.Column(db.Double, nullable = True)
    TitularAU = db.Column(db.String(5), nullable = True)
    DeclaracionPatrimonial = db.Column(db.String(5), nullable = True)
    PlazasSubordinadas = db.Column(db.Integer, nullable = True)
    PuestoJefe = db.Column(db.String(50), nullable = True)
    PresupuestalJefe = db.Column(db.String(15), nullable = True)
    idCentroCosto = db.Column(db.Integer, db.ForeignKey(kCentroCostos.idCentroCosto), nullable = True)

    # Relaciones
    UA = db.relationship('kUA', back_populates = "Puestos", uselist = False, single_parent = True)
    ZonaEconomica = db.relationship('kZonaEconomica', back_populates = "Puestos", uselist = False, single_parent = True)
    TipoPlazaPuesto = db.relationship('kTipoPlazaPuesto', back_populates = "Puestos", uselist = False, single_parent = True)
    CaracterOcupacional = db.relationship('kCaracterOcupacional', back_populates = "Puestos", uselist = False, single_parent = True)
    # RTipoFuncion = db.relationship('TipoFuncion', back_populates = "Puestos", uselist = False, single_parent = True)
    Grupo = db.relationship('kGrupo', back_populates = "Puestos", uselist = False, single_parent = True)
    Grado = db.relationship('kGrado', back_populates = "Puestos", uselist = False, single_parent = True)
    Nivel = db.relationship('kNivel', back_populates = "Puestos", uselist = False, single_parent = True)
    CentroTrabajo = db.relationship('kCentroTrabajo', back_populates = "Puestos", uselist = False, single_parent = True)
    CentroCostos = db.relationship('kCentroCostos', back_populates = "Puestos", uselist = False, single_parent = True)
    EstatusPuesto = db.relationship('kEstatusPuesto', back_populates = "Puestos", uselist = False, single_parent = True)
    Vigencia = db.relationship('kVigencia', back_populates = "Puestos", uselist = False, single_parent = True)

    EmpleadoPuestos = db.relationship("rEmpleadoPuesto", back_populates = "Puesto", cascade = "all, delete-orphan")

    def __init__(self, idPuesto, ConsecutivoPuesto, ReferenciaTabular, Puesto, idUA, idZonaEconomica, idTipoPlazaPuesto,
                 idCaracterOcupacional, idTipoFuncion, idGrupo, idGrado, idNivel, idCentroTrabajo, idCentroCosto, idEstatusPuesto, idVigencia):
        self.idPuesto = idPuesto
        self.ConsecutivoPuesto = ConsecutivoPuesto
        self.ReferenciaTabular = ReferenciaTabular
        self.Puesto = Puesto
        # self.idRamo = idRamo
        self.idUA = idUA
        self.idZonaEconomica = idZonaEconomica
        self.idTipoPlazaPuesto = idTipoPlazaPuesto
        self.idCaracterOcupacional = idCaracterOcupacional
        self.idTipoFuncion = idTipoFuncion
        self.idGrupo = idGrupo
        self.idGrado = idGrado
        self.idNivel = idNivel
        self.idCentroTrabajo = idCentroTrabajo
        self.idCentroCosto = idCentroCosto
        self.idEstatusPuesto = idEstatusPuesto

class rEmpleado(db.Model):
    __tablename__ = "rempleado"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey(tPersona.idPersona), primary_key = True)
    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    NumeroEmpleado = db.Column(db.Integer, nullable = True)
    NoISSSTE = db.Column(db.Integer, nullable = True)
    FecAltaISSSTE = db.Column(db.Date, nullable = True) 
    CorreoInstitucional = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    # Relacion
    Persona = db.relationship("tPersona", back_populates = "Empleado", single_parent = True, cascade = "all, delete-orphan")
    EmpleadoPuestos = db.relationship("rEmpleadoPuesto", back_populates = "Empleado", cascade = "all, delete-orphan")

    def __init__(self, idPersona, idTipoEmpleado, NumeroEmpleado, Activo):
        self.idPersona = idPersona
        self.idTipoEmpleado = idTipoEmpleado
        self.NumeroEmpleado = NumeroEmpleado
        self.NoISSSTE = NoISSSTE
        self.FecAltaISSSTE = FecAltaISSSTE
        self.CorreoInstitucional = CorreoInstitucional
        self.Activo = Activo

class rEmpleadoPuesto(db.Model):
    __tablename__ = "rempleadopuesto"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey(rEmpleado.idPersona), primary_key = True)
    idPuesto = db.Column(db.Integer, db.ForeignKey(tPuesto.ConsecutivoPuesto), primary_key = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relacion
    Empleado = db.relationship("rEmpleado", back_populates = "EmpleadoPuestos", uselist = False, single_parent = True)
    Puesto = db.relationship("tPuesto", back_populates = "EmpleadoPuestos", uselist = False, single_parent = True)

    def __init__(self, idPersona, idPuesto, FechaInicio, FechaFin, Activo):
        self.idPersona = idPersona
        self.idPuesto = idPuesto
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.Activo = Activo

class rBancoPersona(db.Model):
    __tablename__ = "rbancopersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    Clabe = db.Column(db.String(18), primary_key = True)
    Banco = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)
    Verificado = db.Column(db.Boolean, nullable = True)

    def __init__(self, idPersona, Clabe, Banco, Activo, Verificado):
        self.idPersona = idPersona
        self.Clabe = Clabe
        self.Banco = Banco
        self.Activo = Activo
        self.Verificado = Verificado

class rSerieNomina(db.Model):
    __tablename__ = 'rserienomina'
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}
    idNomina = db.Column(db.Integer, primary_key = True)
    SerieInicial = db.Column(db.Integer, nullable = True)
    SerieFinal = db.Column(db.Integer, nullable= True)
    TotalRegistros = db.Column(db.Integer, nullable = True)
    FechaProceso = db.Column(db.Date, nullable = True)

    def __init__(self, idNomina, SerieInicial, SerieFinal, TotalRegistros, FechaProceso):
        self.idNomina = idNomina
        self.SerieInicial = SerieInicial
        self.SerieFinal = SerieFinal
        self.TotalRegistros = TotalRegistros
        self.FechaProceso = FechaProceso