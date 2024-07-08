from app import db
from catalogos.modelos.modelos import *

class tPersona(db.Model):
    __tablename__ = "tpersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    CURP = db.Column(db.String(18), nullable = False)
    Nombre = db.Column(db.String(50), nullable = False)
    ApPaterno = db.Column(db.String(50), nullable = False)
    ApMaterno = db.Column(db.String(50), nullable = False)
    Sexo = db.Column(db.String(15), nullable = True)
    FechaNacimiento = db.Column(db.Date, nullable = True)
    RFC = db.Column(db.String(13), nullable = False)
    idNacionalidad = db.Column(db.Integer, nullable = True)
    CalidadMigratoria = db.Column(db.String(100), nullable = True)
    TelCasa = db.Column(db.String(10), nullable = True)
    TelCelular = db.Column(db.String(10), nullable = True)
    idTipoPersona = db.Column(db.Integer, db.ForeignKey(kTipoPersona.idTipoPersona), nullable = False)
    idEstadoCivil = db.Column(db.Integer, nullable = True)
    CorreoPersonal = db.Column(db.String(150), nullable = True)

    # Relaciones
    TipoPersona = db.relationship("kTipoPersona", back_populates = "Personas", uselist = False, single_parent = True)
    Empleado = db.relationship("rEmpleado", uselist = False, back_populates = "Persona", cascade = "all, delete-orphan", single_parent = True)
    Domicilios = db.relationship("rDomicilio", back_populates = "Persona", cascade = "all, delete-orphan")
    Escolaridades = db.relationship("rPersonaEscolaridad", back_populates = "Persona", cascade = "all, delete-orphan")

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

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class tPuesto(db.Model):
    __tablename__ = "tpuesto"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idRamo = db.Column(db.Integer, nullable = True)
    idUA = db.Column(db.Integer, db.ForeignKey(kUA.idUA), nullable = True)
    ConsecutivoPuesto = db.Column(db.Integer, primary_key = True)
    CodigoPuesto = db.Column(db.String(50), primary_key = True)
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
    Activo = db.Column(db.Integer, nullable = True)

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

    def __init__(self, idRamo, idUA, ConsecutivoPuesto, CodigoPuesto, Puesto, idZonaEconomica, ReferenciaTabular, ConsPuesto, idTipoPlazaPuesto,
                 idCaracterOcupacional, idTipoFuncion, NivelSalarial, Tabulador, CodigoPresupuestal, OrdinalCP, idGrupo, idGrado, idNivel, idEstatusPuesto, 
                 idVigencia, FechaInicio, FechaFin, idCentroTrabajo, FolioSival, RegimenLaboral, RemuneracionTotal, TitularAU, DeclaracionPatrimonial,
                 PlazasSubordinadas, PuestoJefe, PresupuestalJefe, idCentroCosto, Activo):
        self.idRamo = idRamo
        self.idUA = idUA
        self.ConsecutivoPuesto = ConsecutivoPuesto
        self.CodigoPuesto = CodigoPuesto
        self.Puesto = Puesto
        self.idZonaEconomica = idZonaEconomica
        self.ReferenciaTabular = ReferenciaTabular
        self.ConsPuesto = ConsPuesto
        self.idTipoPlazaPuesto = idTipoPlazaPuesto
        self.idCaracterOcupacional = idCaracterOcupacional
        self.idTipoFuncion = idTipoFuncion
        self.NivelSalarial = NivelSalarial
        self.Tabulador = Tabulador
        self.CodigoPresupuestal = CodigoPresupuestal
        self.OrdinalCP = OrdinalCP
        self.idGrupo = idGrupo
        self.idGrado = idGrado
        self.idNivel = idNivel
        self.idEstatusPuesto = idEstatusPuesto
        self.idVigencia = idVigencia
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.idCentroTrabajo = idCentroTrabajo
        self.FolioSival = FolioSival
        self.RegimenLaboral = RegimenLaboral
        self.RemuneracionTotal = RemuneracionTotal
        self.TitularAU = TitularAU
        self.DeclaracionPatrimonial = DeclaracionPatrimonial
        self.PlazasSubordinadas = PlazasSubordinadas
        self.PuestoJefe = PuestoJefe
        self.PresupuestalJefe = PresupuestalJefe
        self.idCentroCosto = idCentroCosto
        self.Activo = Activo
        

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rEmpleado(db.Model):
    __tablename__ = "rempleado"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey(tPersona.idPersona), primary_key = True)
    NumeroEmpleado = db.Column(db.Integer, nullable = False)
    idTipoEmpleado = db.Column(db.Integer, nullable = True)
    idTipoAlta = db.Column(db.Integer, nullable = True)
    idGrupo = db.Column(db.Integer, nullable = True)
    HoraEntrada = db.Column(db.String(20), nullable = True)
    HoraSalida = db.Column(db.String(20), nullable = True)
    FecIngGobierno = db.Column(db.Date, nullable = True)
    FecIngFonaes = db.Column(db.Date, nullable = True)
    idQuincena = db.Column(db.Integer, nullable = True)
    NoISSSTE = db.Column(db.BigInteger, nullable = True)
    FecAltaISSSTE = db.Column(db.Date, nullable = True)
    CorreoInstitucional = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Integer, nullable = False)

    # Relacion
    Persona = db.relationship("tPersona", back_populates = "Empleado", single_parent = True, cascade = "all, delete-orphan")
    EmpleadoPuestos = db.relationship("rEmpleadoPuesto", back_populates = "Empleado", cascade = "all, delete-orphan")
    DiasPersona = db.relationship("rDiasPersona", back_populates = "Empleado", cascade = "all, delete-orphan")
    Banco = db.relationship("rBancoPersona", back_populates = "Empleado", cascade = "all, delete-orphan")

    def __init__(self, idPersona, NumeroEmpleado, idTipoEmpleado, idTipoAlta, idGrupo, HoraEntrada, HoraSalida, FecIngGobierno, FecIngFonaes, idQuincena, NoISSSTE, FecAltaISSSTE, CorreoInstitucional, Activo):
        self.idPersona = idPersona
        self.NumeroEmpleado = NumeroEmpleado
        self.idTipoEmpleado = idTipoEmpleado
        self.idTipoAlta = idTipoAlta
        self.idGrupo = idGrupo
        self.HoraEntrada = HoraEntrada
        self.HoraSalida = HoraSalida
        self.FecIngGobierno = FecIngGobierno
        self.FecIngFonaes = FecIngFonaes
        self.idQuincena = idQuincena
        self.NoISSSTE = NoISSSTE
        self.FecAltaISSSTE = FecAltaISSSTE
        self.CorreoInstitucional = CorreoInstitucional
        self.Activo = Activo

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rEmpleadoPuesto(db.Model):
    __tablename__ = "rempleadopuesto"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey(rEmpleado.idPersona), primary_key = True)
    idPuesto = db.Column(db.Integer, db.ForeignKey(tPuesto.ConsecutivoPuesto), primary_key = True)
    ClavePresupuestaSIA = db.Column(db.String(50), nullable = True)
    CodigoPlazaSia = db.Column(db.String(50), nullable = True)
    CodigoPuestoSIA = db.Column(db.String(25), nullable = True)
    RHNETSIA = db.Column(db.String(25), nullable = True)
    idNivel = db.Column(db.Integer, nullable = True)
    FechaInicio = db.Column(db.Date, primary_key = True)
    FechaTermino = db.Column(db.Date, nullable = True)
    idCausaBaja = db.Column(db.Integer, nullable = False)
    Observaciones = db.Column(db.String(300), nullable = False)
    FechaEfecto = db.Column(db.Date, nullable = False)
    idQuincena = db.Column(db.Integer, nullable = False)
    idEstatusEP = db.Column(db.Integer, primary_key = True) # ACTIVO o INACTIVO

    # Relacion
    Empleado = db.relationship("rEmpleado", back_populates = "EmpleadoPuestos", uselist = False, single_parent = True)
    Puesto = db.relationship("tPuesto", back_populates = "EmpleadoPuestos", uselist = False, single_parent = True)

    def __init__(self, idPersona, idPuesto, ClavePresupuestaSIA, CodigoPlazaSIA, CodigoPuestoSIA, RHNETSIA, idNivel, FechaInicio, FechaTermino, idCausaBaja, Observaciones, FechaEfecto, idQuincena, idEstatusEP):
        self.idPersona = idPersona
        self.idPuesto = idPuesto
        self.ClavePresupuestaSIA = ClavePresupuestaSIA
        self.CodigoPlazaSia = CodigoPlazaSIA
        self.CodigoPuestoSIA = CodigoPuestoSIA
        self.RHNETSIA = RHNETSIA
        self.idNivel = idNivel
        self.FechaInicio = FechaInicio
        self.FechaTermino = FechaTermino
        self.idCausaBaja = idCausaBaja
        self.Observaciones = Observaciones
        self.FechaEfecto = FechaEfecto
        self.idQuincena = idQuincena
        self.idEstatusEP = idEstatusEP

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rPersonaEscolaridad(db.Model):
    __tablename__ = "rpersonaescolaridad"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey('tpersona.idPersona'), primary_key = True)
    idEscolaridad = db.Column(db.Integer, nullable = True)
    idNivelEscolaridad = db.Column(db.Integer, nullable = True)
    idInstitucionEscolar = db.Column(db.Integer, nullable = True)
    idFormacionEducativa = db.Column(db.Integer, nullable = True)
    Especialidad = db.Column(db.Text, nullable = True)
    Consecutivo = db.Column(db.Integer, nullable = True)

    # Relacion
    Persona = db.relationship('tPersona', back_populates = "Escolaridades", uselist = False, single_parent = True)

    def __init__(self, idPersona, idEscolaridad, idNivelEscolaridad, idInstitucionEscolar, idFormacionEducativa, Especialidad, Consecutivo):
        self.idPersona = idPersona
        self.idEscolaridad = idEscolaridad
        self.idNivelEscolaridad = idNivelEscolaridad
        self.idInstitucionEscolar = idInstitucionEscolar
        self.idFormacionEducativa = idFormacionEducativa
        self.Especialidad = Especialidad
        self.Consecutivo = Consecutivo

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rBancoPersona(db.Model):
    __tablename__ = "rbancopersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci", "schema": "db2"}

    idPersona = db.Column(db.Integer, db.ForeignKey(rEmpleado.idPersona), primary_key = True)
    idBanco = db.Column(db.String(50), db.ForeignKey(kBancos.idBanco), nullable = True)
    Clabe = db.Column(db.String(18), primary_key = True)
    NumeroCuenta = db.Column(db.Integer, nullable = True)
    FechaAlta = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    Activo = db.Column(db.Integer, nullable = True)
    Verificado = db.Column(db.Integer, nullable = True)

    # Relacion
    Banco = db.relationship("kBancos", back_populates = "BancoPersonas", uselist = False, single_parent = True)
    Empleado = db.relationship("rEmpleado", back_populates = "Banco", uselist = False, single_parent = True)

    def __init__(self, idPersona, Clabe, idBanco, Activo, Verificado):
        self.idPersona = idPersona
        self.Clabe = Clabe
        self.idBanco = idBanco
        self.Activo = Activo
        self.Verificado = Verificado

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

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

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rPersonaExpediente(db.Model):
    __tablename__ = "rpersonaexpediente"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    ActaNacimiento = db.Column(db.Integer, nullable = True)
    Titulo = db.Column(db.Integer, nullable = True)
    CartillaMilitar = db.Column(db.Integer, nullable = True)
    ComprobanteDomicilio = db.Column(db.Integer, nullable = True)
    IdentificacionOficial = db.Column(db.Integer, nullable = True)
    ArchivoCURP = db.Column(db.Integer, nullable = True)
    ArchivoRFC = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, ActaNacimiento, Titulo, CartillaMilitar, ComprobanteDomicilio, IdentificacionOficial, ArchivoCURP, ArchivoRFC):
        self.idPersona = idPersona
        self.ActaNacimiento = ActaNacimiento
        self.Titulo = Titulo
        self.CartillaMilitar = CartillaMilitar
        self.ComprobanteDomicilio = ComprobanteDomicilio
        self.IdentificacionOficial = IdentificacionOficial
        self.ArchivoCURP = ArchivoCURP
        self.ArchivoRFC = ArchivoRFC

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rPersonaMasInformacion(db.Model):
    __tablename__ = "rpersonamasinformacion"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idIdioma = db.Column(db.Integer, nullable = True)
    idIdiomaIndigena = db.Column(db.Integer, nullable = True)
    idAfroamericano = db.Column(db.Integer, nullable = True)
    idDiscapacidad = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, idIdioma, idIdiomaIndigena, idAfroamericano, idDiscapacidad):
        self.idPersona = idPersona
        self.idIdioma = idIdioma
        self.idIdiomaIndigena = idIdiomaIndigena
        self.idAfroamericano = idAfroamericano
        self.idDiscapacidad = idDiscapacidad

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rPersonaIdioma(db.Model):
    __tablename__ = "rpersonaidioma"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idIdioma = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPersona, idIdioma):
        self.idPersona = idPersona
        self.idIdioma = idIdioma

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rPersonaIndigena(db.Model):
    __tablename__ = "rpersonaindigena"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idIndigena = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPersona, idIndigena):
        self.idPersona = idPersona
        self.idIndigena = idIndigena

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)