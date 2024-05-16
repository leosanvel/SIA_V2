from app import db

class rEmpleadoConcepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    Contrato = db.Column(db.String(25))
    Porcentaje = db.Column(db.Numeric(11, 3))
    Monto = db.Column(db.Numeric(11, 2))
    FechaInicio = db.Column(db.Date)
    FechaFin = db.Column(db.Date)

    def __init__(self, idPersona, idTipoConcepto, idConcepto, Contrato, Porcentaje, Monto, FechaInicio, FechaFin):
        self.idPersona = idPersona
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Contrato = Contrato
        self.Porcentaje = Porcentaje
        self.Monto = Monto
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)