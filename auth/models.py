from flask_login import UserMixin

from app import db

class Tusuario(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'tusuario'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idPersona = db.Column(db.Integer, primary_key = True, unique = True)
    usuario = db.Column(db.String(32), nullable = False)
    contrasena = db.Column(db.String(32), nullable = False)
    estatus = db.Column(db.Integer, nullable = False)
    ultimacontrasena = db.Column(db.String(32), nullable = False)
    fechaalta = db.Column(db.Date, nullable = False)
    idRol = db.Column(db.Integer, nullable = False)
    idPerfil = db.Column(db.Integer, nullable = False)
    	
    def __init__(self,idPersona, usuario, contrasena, estatus, ultimacontrasena, fechaalta,idRol,idPerfil):
        self.idPersona = idPersona
        self.usuario = usuario
        self.contrasena = contrasena
        self.estatus = estatus
        self.ultimacontrasena = ultimacontrasena
        self.fechaalta = fechaalta
        self.idRol = idRol
        self.idPerfil = idPerfil


        # Define la clase User usada para administrar la sesión
class User(UserMixin):
    def __init__(self, user_db):
        self.id = user_db.idPersona
        self.idPersona = user_db.idPersona
        self.usuario = user_db.usuario
        self.contrasena = user_db.contrasena
        self.estatus = user_db.estatus
        self.ultimacontrasena = user_db.ultimacontrasena
        self.fechaalta = user_db.fechaalta
        self.idRol = user_db.idRol
        self.idPerfil = user_db.idPerfil