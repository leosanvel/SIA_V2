from app import db

class tNomina(db.Model):
    __tablename__ = "tnomina"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idNomina = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, nullable = True)
    Nomina = db.Column(db.String(10), nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    Estatus = db.Column(db.Integer, nullable = True)
    Fecha = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    FechaPago = db.Column(db.Date, nullable = True)
    idPersonaEmisor = db.Column(db.Integer, nullable = True)
    PeriodoQuincena = db.Column(db.Integer, nullable = True)
    SMM = db.Column(db.Numeric(11, 2), nullable = True)
    SueldoMensual = db.Column(db.Numeric(11, 2), nullable = True)

    def __init__(self, idQuincena, Nomina, Descripcion, Estatus, FechaPago, idPersonaEmisor, PeriodoQuincena, SMM, SueldoMensual):
        # self.idNomina = idNomina
        self.idQuincena = idQuincena
        self.Nomina = Nomina
        self.Descripcion = Descripcion
        self.Estatus = Estatus
        self.FechaPago = FechaPago
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