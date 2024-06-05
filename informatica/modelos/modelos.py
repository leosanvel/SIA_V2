from app import db

class rSolicitudEstado(db.Model):
    __tablename__ = 'rsolicitudestado'
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}
    idSolicitud = db.Column(db.Integer, primary_key = True)
    Solicitud = db.Column(db.String(100), nullable = False)
    Descripcion = db.Column(db.String(100), nullable = False)
    idEstadoSolicitud = db.Column(db.Integer, nullable = False)
   
    def __init__(self, idSolicitud, Solicitud, Descripcion, idEstadoSolicitud):
        self.idSolicitud = idSolicitud
        self.Solicitud = Solicitud
        self.Descripcion = Descripcion
        self.idEstadoSolicitud = idEstadoSolicitud

    # Actualizar Registro
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)