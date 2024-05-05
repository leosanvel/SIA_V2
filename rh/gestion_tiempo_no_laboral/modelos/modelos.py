from app import db

class kDiasFestivos(db.Model):
    __tablename__ = "kdiasfestivos"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idDiaFestivo = db.Column(db.Integer, primary_key = True)
    Fecha = db.Column(db.Date, nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    FechaCreacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __init__(self, Fecha, Descripcion):
        #self.idDiaFestivo = idDiaFestivo
        self.Fecha = Fecha
        self.Descripcion = Descripcion

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)