from app import db

class tNomina(db.Model):
    __tablename__ = "tnomina"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idTipoNomina = db.Column(db.String(1), nullable = False)
    idQuincena = db.Column(db.Integer, nullable = False)
    Nomina = db.Column(db.String(10), nullable = False)
    Descripcion = db.Column(db.String(100), nullable = False)
    Observaciones = db.Column(db.String(50), nullable = False)
    Estatus = db.Column(db.Integer, nullable = False)
    Fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    FechaPago = db.Column(db.Date, nullable = True)
    FechaInicial = db.Column(db.Date, nullable = True)
    FechaFinal = db.Column(db.Date, nullable = True)
    Quincena = db.Column(db.String(2), nullable = False)
    idPersonaEmisor = db.Column(db.Integer, nullable = False)
    PeriodoQuincena = db.Column(db.Integer, nullable = False)
    SMM = db.Column(db.Numeric(11, 2), nullable = False)
    SueldoMensual = db.Column(db.Numeric(11, 2), nullable = False)

    def __init__(self, idNomina, idTipoNomina, idQuincena, Nomina, Descripcion, Observaciones, Estatus, FechaPago, FechaInicial, FechaFinal, Quincena, idPersonaEmisor, PeriodoQuincena, SMM, SueldoMensual):
        self.idNomina = idNomina
        self.idTipoNomina = idTipoNomina
        self.idQuincena = idQuincena
        self.Nomina = Nomina
        self.Descripcion = Descripcion
        self.Observaciones = Observaciones
        self.Estatus = Estatus
        self.FechaPago = FechaPago
        self.FechaInicial = FechaInicial
        self.FechaFinal = FechaFinal
        self.Quincena = Quincena
        self.idPersonaEmisor = idPersonaEmisor
        self.PeriodoQuincena = PeriodoQuincena
        self.SMM = SMM
        self.SueldoMensual = SueldoMensual

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rNominaPersonas(db.Model):
    __tablename__ = "rnominapersonas"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, primary_key = True)
    idCentroCosto = db.Column(db.Integer, nullable = False)
    idNivel = db.Column(db.Integer, nullable = False)
    idTipoConcepto = db.Column(db.String(1), nullable = False)
    idConcepto = db.Column(db.String(5), nullable = False)
    Importe = db.Column(db.Numeric(11, 2), nullable = False)

    def __init__(self, idNomina, idPersona, idCentroCosto, idNivel, idTipoConcepto, idConcepto, Importe):
        self.idNomina = idNomina
        self.idPersona = idPersona
        self.idCentroCosto = idCentroCosto
        self.idNivel = idNivel
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Importe = Importe

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rDiasRetroactivo(db.Model):
    __tablename__ = "rdiasretroactivo"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, primary_key = True)
    Dias = db.Column(db.Integer, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)

    def __init__(self, idPersona, idQuincena, Dias, Descripcion):
        self.idPersona = idPersona
        self.idQuincena = idQuincena
        self.Dias = Dias
        self.Descripcion = Descripcion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class tFechasCalendario(db.Model):
    __tablename__ = "tfechascalendario"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idMes = db.Column(db.Integer, primary_key = True)
    idQuincenaCalendario = db.Column(db.Integer, primary_key = True)
    idActividadCalendario = db.Column(db.Integer, primary_key = True)
    Periodo = db.Column(db.Integer, primary_key = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)

    def __init__(self, idMes, idQuincenaCalendario, idActividadCalendario, Periodo, FechaInicio, FechaFin):
        self.idMes = idMes
        self.idQuincenaCalendario = idQuincenaCalendario
        self.idActividadCalendario = idActividadCalendario
        self.Periodo = Periodo
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)


class rDiasLaborados(db.Model):
    __tablename__ = "rdiaslaborados"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, primary_key = True)
    DiasLaborados = db.Column(db.Integer, nullable = True)

    def __init__(self, idNomina, idPersona, DiasLaborados):
        self.idNomina = idNomina
        self.idPersona = idPersona
        self.DiasLaborados = DiasLaborados

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)                

class rZonaEconomica(db.Model):
    __tablename__ = "rzonaeconomica"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idAnioFiscal = db.Column(db.Integer, primary_key = True)
    idZonaEconomica = db.Column(db.Integer, primary_key = True)
    idNivel =  db.Column(db.Integer, primary_key = True)
    SueldoBase = db.Column(db.Numeric(11, 2), nullable = False)
    CompensacionGarantizada = db.Column(db.Numeric(11, 2), nullable = False)

    def __init__(self, idAnioFiscal, idZonaEconomica, idNivel, SueldoBase, CompensacionGarantizada):
        self.idAnioFiscal = idAnioFiscal
        self.idZonaEconomica = idZonaEconomica
        self.idNivel = idNivel
        self.SueldoBase = SueldoBase
        self.CompensacionGarantizada = CompensacionGarantizada
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rTabuladorSalarial(db.Model):
    __tablename__ = "rtabuladorsalarial"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idAnioFiscal = db.Column(db.Integer, primary_key = True)
    idGrupo = db.Column(db.String(1), primary_key = True)
    idGrado = db.Column(db.Integer, primary_key = True)
    idNivel =  db.Column(db.Integer, primary_key = True)
    PuntoInicial = db.Column(db.Numeric(11, 2), nullable = False)
    PuntoFinal = db.Column(db.Numeric(11, 2), nullable = False)
    SueldoBase = db.Column(db.Numeric(11, 2), nullable = False)
    CompensacionGarantizada = db.Column(db.Numeric(11, 2), nullable = False)

    def __init__(self, idAnioFiscal, idGrupo, idGrado, idNivel, PuntoInicial, PuntoFinal, SueldoBase, CompensacionGarantizada):
        self.idAnioFiscal = idAnioFiscal
        self.idGrupo = idGrupo
        self.idGrado = idGrado
        self.idNivel = idNivel
        self.PuntoInicial = PuntoInicial
        self.PuntoFinal = PuntoFinal
        self.SueldoBase = SueldoBase
        self.CompensacionGarantizada = CompensacionGarantizada
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
