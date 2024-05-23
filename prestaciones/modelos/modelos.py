from app import db

class rDiasRetroactivo(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rdiasretroactivo"
    __table_arg__ = {"mysql_engine":"InnoDB","mysql_charset":"utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idQuincena = db.Column(db.Integer, primary_key = True)
    Dias = db.Column(db.Integer)
    Descripcion =  db.Column(db.String(25))

    def __init__(self, idPersona, idQuincena, Dias, Descripcion):
        self.idPersona = idPersona
        self.idQuincena = idQuincena
        self.Dias = Dias
        self.Descripcion = Descripcion
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rEmpleadoConcepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    NumeroContrato = db.Column(db.String(25), primary_key = True)
    Porcentaje = db.Column(db.Numeric(11, 3))
    Monto = db.Column(db.Numeric(11, 2))
    FechaInicio = db.Column(db.Date, nullable=True)
    FechaFin = db.Column(db.Date, nullable=True)
    
    def __init__(self, idPersona, idTipoConcepto, idConcepto, NumeroContrato, Porcentaje, Monto, FechaInicio, FechaFin):
        self.idPersona = idPersona
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.NumeroContrato = NumeroContrato
        self.Porcentaje = Porcentaje
        self.Monto = Monto
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