from app import db

class tNomina(db.Model):
    __tablename__ = "tnomina"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, nullable = True)
    Nomina = db.Column(db.String(10))
    Descripcion = db.Column(db.Text, nullable = True)
    Estatus = db.Column(db.Integer, nullable = True)
    Fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    FechaPago = db.Column(db.Date)
    FechaInicial = db.Column(db.Date)
    FechaFinal = db.Column(db.Date)
    Quincena = db.Column(db.String(2))
    idPersonaEmisor = db.Column(db.Integer, nullable = True)
    PeriodoQuincena = db.Column(db.Integer, nullable = True)

    def __init__(self, idNomina, idQuincena, Nomina, Descripcion, Estatus, Fecha,FechaPago, FechaInicial, FechaFinal, Quincena, idPersonaEmisor, PeriodoQuincena):
        self.idNomina = idNomina
        self.idQuincena = idQuincena
        self.Nomina = Nomina
        self.Descripcion = Descripcion
        self.Estatus = Estatus
        self.Fecha = Fecha
        self.FechaPago
        self.FechaInicial = FechaInicial
        self.FechaFinal = FechaFinal
        self.Quincena = Quincena
        self.idPersonaEmisor = idPersonaEmisor
        self.PeriodoQuincena = PeriodoQuincena

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