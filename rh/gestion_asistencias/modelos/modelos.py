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

    def __init__(self, idIncidencia, idPersona, idTipo, Descripcion, FechaInicio, FechaFin):
        self.idIncidencia = idIncidencia
        self.idPersona = idPersona
        self.idTipo = idTipo
        self.Descripcion = Descripcion
        self. FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        # self.FechaCreacion = FechaCreacion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rSancionPersona(db.Model):
    __tablename__ = "rsancionpersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idSancionPersona = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, nullable = True)
    idSancion = db.Column(db.Integer, nullable = True)
    idPorcentaje = db.Column(db.Integer, nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    FechaInicioDescuento = db.Column(db.Date, nullable = True)
    FechaFinDescuento = db.Column(db.Date, nullable = True)
    Dias = db.Column(db.Integer, nullable = True)
    FechaCreacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    Descripcion = db.Column(db.Text, nullable = True)
    idQuincena = db.Column(db.Integer, nullable = False)

    def __init__(self, idSancionPersona = None, idPersona = None, idSancion = None, idPorcentaje = None, FechaInicio = None, FechaFin = None, FechaInicioDescuento = None, FechaFinDescuento = None, Dias= None, Descripcion = None, idQuincena = None):
        self.idSancionPersona = idSancionPersona
        self.idPersona = idPersona
        self.idSancion = idSancion
        self.idPorcentaje = idPorcentaje
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.FechaInicioDescuento = FechaInicioDescuento
        self.FechaFinDescuento = FechaFinDescuento
        self.Dias = Dias
        # self.FechaCreacion = FechaCreacion
        self.Descripcion = Descripcion
        self.idQuincena = idQuincena

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class tJustificante(db.Model):
    __tablename__ = "tjustificante"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idJustificante = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, nullable = True)
    idTipo = db.Column(db.Integer, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    FechaCreacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, idJustificante, idPersona, idTipo, Descripcion, FechaInicio, FechaFin):
        self.idJustificante = idJustificante
        self.idPersona = idPersona
        self.idTipo = idTipo
        self.Descripcion = Descripcion
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

# class tIncidenciasPasadas(db.Model):
#     __tablename__ = "tincidenciaspasadas"
#     __bind_key__ = 'db2'
#     __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

#     idIncidenciaPasada = db.Column(db.Integer, primary_key = True)
#     idPersona = db.Column(db.Integer, nullable = False)
#     Fecha = db.Column(db.Date, nullable = False)
#     idQuincena = db.Column(db.Integer, nullable = False)
#     Activo = db.Column(db.Integer, nullable = False)

#     def __init__(self, idIncidenciaPasada, idPersona, Fecha, idQuincena, Activo):
#         self.idIncidenciaPasada = idIncidenciaPasada
#         self.idPersona = idPersona
#         self.Fecha = Fecha
#         self.idQuincena = idQuincena
#         self.Activo = Activo
    
#     def update(self, **kwargs):
#         for attr, value in kwargs.items():
#             if hasattr(self, attr):
#                 setattr(self, attr, value)

class rSepararDiasLicencia(db.Model):
    __tablename__ = "rseparardiaslicencia"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idSancionPersona = db.Column(db.Integer, primary_key = True)
    idPersona = db.Column(db.Integer, primary_key = True)
    Dias = db.Column(db.Integer, nullable = False)
    idQuincena = db.Column(db.Integer, primary_key = True)
    idPorcentaje = db.Column(db.Integer, primary_key = True)

    def __init__(self, idSancionPersona, idPersona, Dias, idQuincena, idPorcentaje):
        self.idSancionPersona = idSancionPersona
        self.idPersona = idPersona
        self.Dias = Dias
        self.idQuincena = idQuincena
        self.idPorcentaje = idPorcentaje

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)