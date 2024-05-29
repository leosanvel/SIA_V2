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

class kMeses(db.Model):
    __tablename__ = "kmeses"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idMes = db.Column(db.Integer, primary_key = True)
    Mes = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idMes, Mes, Activo):
        self.idMes = idMes
        self.Mes = Mes
        self.Activo = Activo

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class kQuincenaCalendario(db.Model):
    __tablename__ = "kquincenacalendario"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idQuincenaCalendario = db.Column(db.Integer, primary_key = True)
    QuincenaCalendario = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idQuincenaCalendario, QuincenaCalendario, Activo):
        self.idQuincenaCalendario = idQuincenaCalendario
        self.QuincenaCalendario = QuincenaCalendario
        self.Activo = Activo

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class kActividadCalendario(db.Model):
    __tablename__ = "kactividadcalendario"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idActividadCalendario = db.Column(db.Integer, primary_key = True)
    ActividadCalendario = db.Column(db.String(200), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idActividadCalendario, ActividadCalendario, Activo):
        self.idActividadCalendario = idActividadCalendario
        self.ActividadCalendario = ActividadCalendario
        self.Activo = Activo

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