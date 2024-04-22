from app import db

class Domicilio(db.Model):
    __tablename__ = "rdomicilio"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoDomicilio = db.Column(db.Integer, primary_key = True)
    CP = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, idTipoDomicilio, CP):
        self.idPersona = idPersona
        self.idTipoDomicilio = idTipoDomicilio
        self.CP = CP

class TipoDomicilio(db.Model):
    __tablename__ = "ktipodomicilio"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoDomicilio = db.Column(db.Integer, primary_key = True)
    TipoDomicilio = db.Column(db.String(50), nullable = True)
    Activo = db.Column(db.Boolean, nullable = True)

    def __init__(self, idTipoDomicilio, TipoDomicilio, Activo):
        self.idTipoDomicilio = idTipoDomicilio
        self.TipoDomicilio = TipoDomicilio
        self.Activo = Activo