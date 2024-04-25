from app import db
from catalogos.modelos.modelos import *

class Persona(db.Model):
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
    idTipoPersona = db.Column(db.Integer, nullable = True)
    idEstadoCivil = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, CURP, Nombre, ApPaterno, ApMaterno, Sexo, FechaNacimiento, RFC, idNacionalidad,
                 CalidadMigratoria, TelCasa, TelCelular, idTipoPersona, idEstadoCivil):
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

class Puesto(db.Model):
    __tablename__ = "tpuesto"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    # idRamo = db.Column(db.Integer, nullable = True)
    idUA = db.Column(db.Integer, db.ForeignKey(UA.idUA), nullable = True)
    ConsecutivoPuesto = db.Column(db.Integer, primary_key = True)
    CodigoPuesto = db.Column(db.String(50), nullable = True)
    Puesto = db.Column(db.String(150), nullable = True)
    idZonaEconomica = db.Column(db.Integer, db.ForeignKey(ZonaEconomica.idZonaEconomica), nullable = True)
    ReferenciaTabular = db.Column(db.String(10), nullable = True)
    ConsPuesto = db.Column(db.Integer, nullable = True)    
    idTipoPlazaPuesto = db.Column(db.Integer, db.ForeignKey(TipoPlazaPuesto.idTipoPlazaPuesto), nullable = True)
    idCaracterOcupacional = db.Column(db.Integer, db.ForeignKey(CaracterOcupacional.idCaracterOcupacional), nullable = True)
    idTipoFuncion = db.Column(db.Integer, nullable = True)
    NivelSalarial = db.Column(db.String(5), nullable = True)
    Tabulador = db.Column(db.Integer, nullable = True)
    CodigoPresupuestal = db.Column(db.String(10), nullable = True)
    OrdinalCP = db.Column(db.Integer, nullable = True)
    idGrupo = db.Column(db.Integer, db.ForeignKey(Grupo.idGrupo), nullable = True)
    idGrado = db.Column(db.Integer, db.ForeignKey(Grado.idGrado), nullable = True)
    idNivel = db.Column(db.Integer, db.ForeignKey(Nivel.idNivel), nullable = True)
    idEstatusPuesto = db.Column(db.Integer, db.ForeignKey(EstatusPuesto.idEstatusPuesto), nullable = True)
    idVigencia = db.Column(db.Integer, db.ForeignKey(Vigencia.idVigencia), nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    idCentroTrabajo = db.Column(db.Integer, db.ForeignKey(CentroTrabajo.idCentroTrabajo), nullable = True)
    FolioSival = db.Column(db.String(15), nullable = True)
    RegimenLaboral = db.Column(db.String(15), nullable = True)
    RemuneracionTotal = db.Column(db.Double, nullable = True)
    TitularAU = db.Column(db.String(5), nullable = True)
    DeclaracionPatrimonial = db.Column(db.String(5), nullable = True)
    PlazasSubordinadas = db.Column(db.Integer, nullable = True)
    PuestoJefe = db.Column(db.String(50), nullable = True)
    PresupuestalJefe = db.Column(db.String(15), nullable = True)
    idCentroCosto = db.Column(db.Integer, db.ForeignKey(CentroCostos.idCentroCosto), nullable = True)

    # Relaciones
    RUA = db.relationship('UA', back_populates = "Puestos", uselist = False, single_parent = True)
    RZonaEconomica = db.relationship('ZonaEconomica', back_populates = "Puestos", uselist = False, single_parent = True)
    RTipoPlazaPuesto = db.relationship('TipoPlazaPuesto', back_populates = "Puestos", uselist = False, single_parent = True)
    RCaracterOcupacional = db.relationship('CaracterOcupacional', back_populates = "Puestos", uselist = False, single_parent = True)
    # RTipoFuncion = db.relationship('TipoFuncion', back_populates = "Puestos", uselist = False, single_parent = True)
    RGrupo = db.relationship('Grupo', back_populates = "Puestos", uselist = False, single_parent = True)
    RGrado = db.relationship('Grado', back_populates = "Puestos", uselist = False, single_parent = True)
    RNivel = db.relationship('Nivel', back_populates = "Puestos", uselist = False, single_parent = True)
    RCentroTrabajo = db.relationship('CentroTrabajo', back_populates = "Puestos", uselist = False, single_parent = True)
    RCentroCostos = db.relationship('CentroCostos', back_populates = "Puestos", uselist = False, single_parent = True)
    REstatusPuesto = db.relationship('EstatusPuesto', back_populates = "Puestos", uselist = False, single_parent = True)
    RVigencia = db.relationship('Vigencia', back_populates = "Puestos", uselist = False, single_parent = True)

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

class Empleado(db.Model):
    __tablename__ = "rempleado"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    NumeroEmpleado = db.Column(db.Integer, nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    # Relacion
    

    def __init__(self, idPersona, idTipoEmpleado, NumeroEmpleado, Activo):
        self.idPersona = idPersona
        self.idTipoEmpleado = idTipoEmpleado
        self.NumeroEmpleado = NumeroEmpleado
        self.Activo = Activo

class EmpleadoPuesto(db.Model):
    __tablename__ = "rempleadopuesto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idPuesto = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPersona, idPuesto):
        self.idPersona = idPersona
        self.idPuesto = idPuesto