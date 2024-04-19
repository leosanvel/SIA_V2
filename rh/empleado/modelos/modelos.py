from app import db

class Tpuesto(db.Model):
    __tablename__ = "tpuesto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPuesto = db.Column(db.Integer, primary_key = True)

    def __init__(self, idPuesto):
        self.idPuesto = idPuesto
