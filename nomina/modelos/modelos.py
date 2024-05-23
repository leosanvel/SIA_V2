from app import db

class tNomina(db.Model):
    __tablename__ = "tnomina"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idTipoNomina = db.Column(db.String(1), nullable = True)
    idQuincena = db.Column(db.Integer, nullable = True)
    Nomina = db.Column(db.String(10), nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    Observaciones = db.Column(db.Text, nullable = True)
    Estatus = db.Column(db.Integer, nullable = True)
    Fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    FechaPago = db.Column(db.Date)
    FechaInicial = db.Column(db.Date)
    FechaFinal = db.Column(db.Date)
    Quincena = db.Column(db.String(2))
    idPersonaEmisor = db.Column(db.Integer, nullable = True)
    PeriodoQuincena = db.Column(db.Integer, nullable = True)
    SMM = db.Column(db.Numeric(11, 2), nullable = True)
    SueldoMensual = db.Column(db.Numeric(11, 2), nullable = True)

    def __init__(self, idNomina, idTipoNomina, idQuincena, Nomina, Descripcion, Observaciones, Estatus, FechaPago, Fecha, FechaInicial, FechaFinal, Quincena, idPersonaEmisor, PeriodoQuincena, SMM, SueldoMensual):
        self.idNomina = idNomina
        self.idTipoNomina = idTipoNomina
        self.idQuincena = idQuincena
        self.Nomina = Nomina
        self.Descripcion = Descripcion
        self.Observaciones = Observaciones
        self.Estatus = Estatus
        self.Fecha = Fecha
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

class rNominaPersona(db.Model):
    __tablename__ = "rnominapersona"
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

class kTipoNomina(db.Model):
    __tablename__ = "ktiponomina"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idTipoNomina = db.Column(db.Integer, primary_key = True)
    TipoNomina = db.Column(db.String(100), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idTipoNomina, TipoNomina, Activo):
        self.idTipoNomina = idTipoNomina
        self.TipoNomina = TipoNomina
        self.Activo = Activo

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

class rNominaPersonas(db.Model):
    __tablename__ = "rnominapersonas"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    idCentroCosto = db.Column(db.Integer, nullable = True)
    idNivel = db.Column(db.Text, nullable = True)
    Importe = db.Column(db.Numeric(11, 2))

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