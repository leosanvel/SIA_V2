from datetime import datetime
from sqlalchemy import func
from app import db
from rh.gestion_empleados.modelos.empleado import Puesto

class CentroCosto(db.Model):
    __tablename__ = "kcentrocosto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idCentroCosto = db.Column(db.Integer, primary_key = True)
    CentroCosto = db.Column(db.String(50), nullable = False)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RCentroCosto", cascade = "all, delete-orphan")

    def __init__(self, idCentroCosto, CentroCosto):
        self.idCentroCosto = idCentroCosto
        self.CentroCosto = CentroCosto

class Grado(db.Model):
    __tablename__ = "kgrado"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}
    
    idGrado = db.Column(db.Integer, primary_key = True)
    Grado = db.Column(db. String(50), nullable = False)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RGrado", cascade = "all, delete-orphan")

    def __init__(self, idGrado, Grado):
        self.idGrado = idGrado
        self.Grado = Grado

class CaracterOcupacional(db.Model):
    __ta1blename__ = "kcaracterocupacional"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idCaracterOcupacional = db.Column(db.Integer, primary_key = True)
    CaracterOcupacional = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RCaracterOcupacional", cascade = "all, delete-orphan")

    def __init__(self, idCaracterOcupacional, CaracterOcupacional, Activo):
        self.idCaracterOcupacional = idCaracterOcupacional
        self.CaracterOcupacional = CaracterOcupacional
        self.Activo = Activo

class Nivel(db.Model):
    __tablename__ = "knivel"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idNivel = db.Column(db.Integer, primary_key = True)
    Nivel = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RNivel", cascade = "all, delete-orphan")

    def __init__(self, idNivel, Nivel, Activo):
        self.idNivel = idNivel
        self.Nivel = Nivel
        self.Activo = Activo

class Grupo(db.Model):
    __tablename__ = "kgrupo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idGrupo = db.Column(db.Integer, primary_key = True)
    Grupo = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RGrupo", cascade = "all, delete-orphan")

    def __init__(self, idGrupo, Grupo, Activo):
        self.idGrupo = idGrupo
        self.Grupo = Grupo
        self.Activo = Activo

class ZonaEconomica(db.Model):
    __tablename__ = "kzonaeconomica"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idZonaEconomica = db.Column(db.Integer, primary_key = True)
    ZonaEconomica = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RZonaEconomica", cascade = "all, delete-orphan")

    def __init__(self, idZonaEconomica, ZonaEconomica, Activo):
        self.idZonaEconomica = idZonaEconomica
        self.ZonaEconomica = ZonaEconomica
        self.Activo = Activo

class Ramo(db.Model):
    __tablename__ = "kramo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idRamo = db.Column(db.Integer, primary_key = True)
    Ramo = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    UAs = db.relationship("UA", back_populates = "Ramo", cascade = "all, delete-orphan")

    def __init__(self, idRamo, Ramo, Activo):
        self.idRamo = idRamo
        self.Ramo = Ramo
        self.Activo = Activo

class UA(db.Model):
    __tablename__ = "kua"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idRamo = db.Column(db.Integer, db.Foreingkey(Ramo.idRamo), nullable = True)
    idUA = db.Column(db.Integer, primary_key = True)
    UA = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    #Relación
    Ramo = db.relationship('Ramo', back_populates = "UAs", uselist = False, single_parent = True)
    Puestos = db.relationship('Puesto', back_populates = "RUA", cascade = "all, delete-orphan")

    def __init__(self, idRamo, idUA, UA, Activo):
        self.idRamo = idRamo
        self.idUA = idUA
        self.UA = UA
        self.Activo = Activo

class EstatusPuesto(db.Model):
    __tablename__ = "kestatuspuesto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idEstatusPuesto = db.Column(db.Integer, primary_key = True)
    EstatusPuesto = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "REstatusPuesto", cascade = "all, delete-orphan")

    def __init__(self, idEstatusPuesto, EstatusPuesto, Activo):
        self.idEstatusPuesto = idEstatusPuesto
        self.EstatusPuesto = EstatusPuesto
        self.Activo = Activo

class CentroTrabajo(db.Model):
    __tablename__ = "kcentrotrabajo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idCentroTrabajo = db.Column(db.Integer, primary_key = True)
    CentroTrabajo = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)
    
    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RCentroTrabajo", cascade = "all, delete-orphan")

    def __init__(self, idCentroTrabajo, CentroTrabajo, Activo):
        self.idCentroTrabajo = idCentroTrabajo
        self.CentroTrabajo = CentroTrabajo
        self.Activo = Activo

class TipoPlazaPuesto(db.Model):
    __tablename__ = "ktipoplaza"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoPlazaPuesto = db.Column(db.Integer, primary_key = True)
    TipoPlazaPuesto = db.Column(db.String(150), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    # Relación
    Puestos = db.relationship('Puesto', back_populates = "RTipoPlazaPuesto", cascade = "all, delete-orphan")

    def __init__(self, idTipoPlazaPuesto, TipoPlazaPuesto, Activo):
        self.idTipoPlazaPuesto = idTipoPlazaPuesto
        self.TipoPlazaPuesto = TipoPlazaPuesto
        self.Activo = Activo

class Vigencia(db.Model):
    __tablename__ = "kvigencia"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idVigencia = db.Column(db.Integer, primary_key = True)
    Vigencia = db.column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    #Relación
    Puestos = db.relationship('Puesto', back_populates = "RVigencia", cascade = "all, delete-orphan")

    def __init__(self, idVigencia, Vigencia, Activo):
        self.idVigencia = idVigencia
        self.Vigencia = Vigencia
        self.Activo = Activo


class Nacionalidad(db.Model):
    __tablename__ = "knacionalidad"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idNacionalidad = db.Column(db.Integer, primary_key = True)
    Nacionalidad = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idNacionalidad, Nacionalidad, Activo):
        self.idNacionalidad = idNacionalidad
        self.Nacionalidad = Nacionalidad
        self.Activo = Activo

class TipoPersona(db.Model):
    __tablename__ = "ktipopersona"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoPersona = db.Column(db.Integer, primary_key = True)
    TipoPersona = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoPersona, TipoPersona, Activo):
        self.idTipoPersona = idTipoPersona
        self.TipoPersona = TipoPersona
        self.Activo = Activo

class TipoEmpleado(db.Model):
    __tablename__ = "ktipoempleado"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoEmpleado = db.Column(db.Integer, primary_key = True)
    TipoEmpleado = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoEmpleado, TipoEmpleado, Activo):
        self.idTipoEmpleado = idTipoEmpleado
        self.TipoEmpleado = TipoEmpleado
        self.Activo = Activo