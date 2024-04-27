from flask_login import UserMixin
from app import db

from autenticacion.modelos.modelos import rUsuario

class kMenu(db.Model):
    __tablename__ = 'kmenu'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, primary_key = True, nullable = False)
    Menu = db.Column(db.String(32), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)

    def __init__(self, Menu = None, Activo = None):
        # self.idMenu = idMenu
        self.Menu = Menu
        self.Activo = Activo

class kSubMenu(db.Model):
    __tablename__ = 'ksubmenu'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, db.ForeignKey(kMenu.idMenu), primary_key=True, nullable = False)
    idSubMenu = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    SubMenu = db.Column(db.String(32), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)

    def __init__(self, idMenu = None, idSubMenu = None, SubMenu = None, Activo = None):
        self.idMenu = idMenu
        self.idSubMenu = idSubMenu
        self.SubMenu = SubMenu
        self.Activo = Activo

class kPagina(db.Model):
    __tablename__ = 'kpagina'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idMenu = db.Column(db.Integer, db.ForeignKey(kMenu.idMenu), primary_key = True, nullable = False)
    idSubMenu = db.Column(db.Integer, db.ForeignKey(kSubMenu.idSubMenu), primary_key = True, nullable = False)
    # idSubMenu = db.Column(db.Integer, nullable = False)
    idPagina = db.Column(db.Integer, primary_key = True, nullable = False)
    Pagina = db.Column(db.String(150), nullable = False)
    URL = db.Column(db.String(150), nullable = False)
    Activo = db.Column(db.Integer, nullable = False)
   
    def __init__(self, idMenu, idSubMenu = None, idPagina = None, Pagina = None, URL = None, Activo = None):
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

    Usuario = db.Column(db.String(50),db.ForeignKey(rUsuario.Usuario),  primary_key=True, nullable=False)
    idMenu = db.Column(db.Integer, db.ForeignKey(kMenu.idMenu),  primary_key=True, nullable=False)  # Definir ForeignKey para establecer la relación
    idSubMenu = db.Column(db.Integer, db.ForeignKey(kSubMenu.idSubMenu),  primary_key=True, nullable=False)
    idPagina = db.Column(db.Integer, db.ForeignKey(kPagina.idPagina),  primary_key=True, nullable=False)
    idPermiso = db.Column(db.Integer, nullable=False)
   
    def __init__(self, Usuario, idMenu, idSubMenu, idPagina, idPermiso):
        self.Usuario = Usuario
        self.idMenu = idMenu
        self.idSubMenu = idSubMenu
        self.idPagina = idPagina
        self.idPermiso = idPermiso