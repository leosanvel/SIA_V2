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
    NumeroContrato = db.Column(db.String(5), primary_key = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)

    def __init__(self, idPersona, idTipoConcepto, idConcepto, Porcentaje, Monto, NumeroContrato, FechaInicio, FechaFin):
        self.idPersona = idPersona
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Contrato = Contrato
        self.Porcentaje = Porcentaje
        self.Monto = Monto
        self.NumeroContrato = NumeroContrato
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)


class rEmpleadoSueldo(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadosueldo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idPuesto = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Salario = db.Column(db.Integer)
    Compensacion = db.Column(db.Integer)

    def __init__(self, idTipoConcepto, idConcepto, NumeroContrato, FechaInicio, FechaFin):
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.NumeroContrato = NumeroContrato
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)