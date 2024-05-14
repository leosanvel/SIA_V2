from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class kDiasFestivos(db.Model):
    __tablename__ = "kdiasfestivos"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idDiaFestivo = db.Column(db.Integer, primary_key = True)
    Fecha = db.Column(db.Date, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    FechaCreacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, Fecha, Descripcion):
        #self.idDiaFestivo = idDiaFestivo
        self.Fecha = Fecha
        self.Descripcion = Descripcion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class kPeriodoVacacional(db.Model):
    __tablename__ = "kperiodovacacional"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPeriodoVacacional = db.Column(db.Integer, primary_key = True)
    idPeriodo = db.Column(db.Integer, nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)

    def __init__(self, idPeriodoVacacional, idPeriodo, FechaInicio, FechaFin, Descripcion):
        self.idPeriodoVacacional = idPeriodoVacacional
        self.idPeriodo = idPeriodo
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.Descripcion = Descripcion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rDiasPersona(db.Model):
    __tablename__ = "rdiaspersona"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey('rempleado.idPersona'), primary_key = True)
    idPeriodo = db.Column(db.Integer, primary_key = True)
    DiasGanados = db.Column(db.Integer, nullable = True)
    Fecha = db.Column(db.Date, primary_key = True)
    Activo = db.Column(db.Integer, nullable = False)

    # Relación
    Empleado = db.relationship('rEmpleado', back_populates = "DiasPersona", uselist = False, single_parent = True)

    def __init__(self, idPersona, idPeriodo, DiasGanados, Fecha, Activo):
        self.idPersona = idPersona
        self.idPeriodo = idPeriodo
        self.DiasGanados = DiasGanados
        self.Fecha = Fecha
        self.Activo = Activo

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rEmpleadoDiasPorciento(db.Model):
    __tablename__ = "rempleadodiasporciento"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, primary_key = True)
    idPorcentaje = db.Column(db.Integer, primary_key = True)
    Dias = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPersona, idQuincena, idPorcentaje, Dias):
        self.idPersona = idPersona
        self.idQuincena = idQuincena
        self.idPorcentaje = idPorcentaje
        self.Dias = Dias

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)