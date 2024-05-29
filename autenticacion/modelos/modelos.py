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
    idPersona = db.Column(db.Integer, nullable = True)
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


