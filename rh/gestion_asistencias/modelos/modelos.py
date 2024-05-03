from app import db

class rPoliticaPersona(db.Model):
    __tablename__ = "rpoliticapersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idPolitica = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPersona, idPolitica):
        self.idPersona = idPersona
        self.idPolitica = idPolitica

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class tChecador(db.Model):
    __tablename__ = "tchecador"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, primary_key = True)
    Fecha = db.Column(db.Date, primary_key = True)
    HoraEntrada = db.Column(db.String(20), nullable = True)
    HoraSalida = db.Column(db.String(20), nullable = True)
    idQuincenaReportada = db.Column(db.Integer, nullable = True)
    idIncidencia = db.Column(db.Integer, nullable = True)
    idJustificante = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, idQuincena, Fecha, HoraEntrada, HoraSalida, idQuincenaReportada, idIncidencia, idJustificante):
        self.idPersona = idPersona
        self.idQuincena = idQuincena
        self.Fecha = Fecha
        self.HoraEntrada = HoraEntrada
        self.HoraSalida = HoraSalida
        self.idQuincenaReportada = idQuincenaReportada
        self.idIncidencia = idIncidencia
        self.idJustificante = idJustificante

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class tIncidencia(db.Model):
    __tablename__ = "tincidencia"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idIncidencia = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, nullable = True)
    idTipo = db.Column(db.Integer, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    FechaCreacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, idIncidencia, idPersona, idTipo, Descripcion, FechaInicio, FechaFin, FechaCreacion):
        self.idIncidencia = idIncidencia
        self.idPersona = idPersona
        self.idTipo = idTipo
        self.Descripcion = Descripcion
        self. FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.FechaCreacion = FechaCreacion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)