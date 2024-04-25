from flask_login import UserMixin
from app import db

        # Define la clase User usada para administrar la sesión
class User(UserMixin):
    def __init__(self, user_db):
        self.id = user_db.Usuario
        self.idPersona = user_db.idPersona
        self.Usuario = user_db.Usuario
        self.Contrasenia = user_db.Contrasenia
        self.PrimerIngreso = user_db.PrimerIngreso
        self.Activo = user_db.Activo


class rUsuario(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'rusuario'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idPersona = db.Column(db.Integer, nullable = False)
    Usuario = db.Column(db.String(32), primary_key = True, nullable = False)
    Contrasenia = db.Column(db.String(32), nullable = False)
    PrimerIngreso = db.Column(db.Date, nullable = False)
    Activo = db.Column(db.Integer, nullable = False)
                     
    def __init__(self, idPersona, Usuario, Contrasenia, PrimerIngreso, Activo):
        self.idPersona = idPersona
        self.Usuario = Usuario
        self.Contrasenia = Contrasenia
        self.PrimerIngreso = PrimerIngreso
        self.Activo = Activo


class Concepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "kconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    Concepto = db.Column(db.String(250), nullable = False)
    Abreviatura = db.Column(db.String(25), nullable = False)
    Porcentaje = db.Column(db.Numeric(11, 3), nullable = True)
    Monto = db.Column(db.Numeric(11, 2), nullable = True)
    ClaveSAT = db.Column(db.String(25), nullable = False)
    idTipoPago = db.Column(db.Integer, nullable = False)
    Activo = db.Column(db.Integer, nullable = False)


    def __init__(self,idTipoConcepto, idConcepto, Concepto, Abreviatura, Porcentaje, Monto, ClaveSAT, idTipoPago, Activo):
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Concepto = Concepto
        self.Abreviatura = Abreviatura
        self.Porcentaje = Porcentaje
        self.Monto = Monto
        self.ClaveSAT = ClaveSAT
        self.idTipoPago = idTipoPago
        self.Activo = Activo

class TipoConcepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "ktipoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    TipoConcepto = db.Column(db.String(25), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idTipoConcepto, TipoConcepto, Activo):
        self.idTipoConcepto = idTipoConcepto
        self.TipoConcepto = TipoConcepto
        self.Activo = Activo

class TipoPago(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "ktipopago"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idTipoPago = db.Column(db.String(1), primary_key = True)
    TipoPago = db.Column(db.String(25), nullable = True)
    Activo = db.Column(db.Integer, nullable = True)

    def __init__(self, idTipoPago, TipoPago, Activo):
        self.idTipoPago = idTipoPago
        self.TipoPago = TipoPago
        self.Activo = Activo

class EmpleadoConcepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.String(1), primary_key = True)
    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    Porcentaje = db.Column(db.Numeric(11, 3))
    Monto = db.Column(db.Numeric(11, 2))

    def __init__(self, idPersona, idTipoConcepto, idConcepto, Porcentaje, Monto):
        self.idPersona = idPersona
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Porcentaje = Porcentaje
        self.Monto = Monto