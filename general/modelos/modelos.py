from flask_login import UserMixin
from app import db

from autenticacion.modelos.modelos import rUsuario
from catalogos.modelos.modelos import kMenu, kSubMenu, kPagina

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

    # Actualizar registro
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)