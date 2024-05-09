from app.general.utils.db import Base
from app import db
class Rsolicitudestado(db.Model):
    __tablename__ = 'rsolicitudestado'
    __bind_key__ = 'db2'
    __table_arg__ = {'mysql_engine':'InnoDB', 'mysql_charset': 'utf8mb4'}
    idSolicitud = db.Column(db.Integer, primary_key = True)
    Solicitud = db.Column(db.String(50), nullable = False)
    Descripcion = db.Column(db.String(50), nullable = False)
    idEstadoSolicitud = db.Column(db.Integer, nullable = False)
   
    def __init__(self, idSolicitud, Solicitud, Descripcion, idEstadoSolicitud):
        self.idSolicitud = idSolicitud
        self.Solicitud = Solicitud
        self.Descripcion = Descripcion
        self.idEstadoSolicitud = idEstadoSolicitud
        

