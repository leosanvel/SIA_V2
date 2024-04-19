from flask_login import UserMixin

from app import db

        # Define la clase User usada para administrar la sesión
class User(UserMixin):
    def __init__(self, user_db):
        self.id = user_db.idPersona
        self.idPersona = user_db.idPersona
        self.Usuario = user_db.Usuario
        self.Contrasenia = user_db.Contrasenia
        self.PrimerIngreso = user_db.PrimerIngreso
        self.Activo = user_db.Activo

#Clases de la base de datos
class rUsuario(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'rusuario'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idPersona = db.Column(db.Integer, primary_key = True, nullable = False)
    idUsuario = db.Column(db.Integer, primary_key = True, nullable = False)
    Usuario = db.Column(db.String(32), nullable = False)
    Contrasenia = db.Column(db.String(32), nullable = False)
    PrimerIngreso = db.Column(db.Date, nullable = False)
    Activo = db.Column(db.Integer, nullable = False)
       	
    def __init__(self,idPersona, Usuario, Contrasena, PrimerIngreso, Activo):
        self.idPersona = idPersona
        self.Usuario = Usuario
        self.Contrasenia = Contrasena
        self.PrimerIngreso = PrimerIngreso
        self.Activo = Activo
        
class kMenu(db.Model):
    __tablename__ = 'kmenu'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    Menu = db.Column(db.String(32), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)
       	
    def __init__(self,idMenu, Menu, Activo):
        self.idMenu = idMenu
        self.Menu = Menu
        self.Activo = Activo

class kSubMenu(db.Model):
    __tablename__ = 'ksubmenu'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    idSubMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    SubMenu = db.Column(db.String(32), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)

    def __init__(self,idMenu,idSubMenu, SubMenu, Activo):
        self.idMenu = idMenu
        self.idSubMenu = idSubMenu
        self.SubMenu = SubMenu
        self.Activo = Activo


class kPagina(db.Model):
    __tablename__ = 'kpagina'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    idSubMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    idPagina = db.Column(db.Integer, primary_key = True, nullable = False)
    Pagina = db.Column(db.String(32), nullable = False)
    URL = db.Column(db.String(32), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)
   

    def __init__(self,idMenu,idSubMenu,idPagina, Pagina, URL, Activo):
        self.idMenu = idMenu
        self.idSubMenu = idSubMenu
        self.idPagina = idPagina
        self.Pagina = Pagina
        self.URL = URL
        self.Activo = Activo

class rPPUsuario(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'rppusuario'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idUsuario = db.Column(db.Integer, primary_key = True, nullable = False)
    idMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    idSubMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    idPagina = db.Column(db.Integer, primary_key = True, nullable = False)
    idPermiso = db.Column(db.Integer, nullable = False)

    
    def __init__(self,idUsuario, idMenu, idSubMenu, idPagina, idPermiso):
        self.idUsuario = idUsuario
        self.idMenu = idMenu
        self.idSubMenu = idSubMenu
        self.idPagina = idPagina
        self.idPermiso = idPermiso

