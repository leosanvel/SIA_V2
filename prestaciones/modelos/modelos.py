from app import db

class rEmpleadoConcepto(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadoconcepto"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idTipoConcepto = db.Column(db.String(1), primary_key = True)
    idConcepto = db.Column(db.String(5), primary_key = True)
    NumeroContrato = db.Column(db.String(15), primary_key = True)
    Porcentaje = db.Column(db.Numeric(11, 3), nullable = True)
    Monto = db.Column(db.Numeric(11, 2), nullable = True)
    FechaInicio = db.Column(db.Date, nullable = True)
    FechaFin = db.Column(db.Date, nullable = True)
    PagoUnico = db.Column(db.Integer, nullable = True)

    def __init__(self, idPersona, idTipoConcepto, idConcepto, Porcentaje, Monto, NumeroContrato, FechaInicio, FechaFin, PagoUnico):
        self.idPersona = idPersona
        self.idTipoConcepto = idTipoConcepto
        self.idConcepto = idConcepto
        self.Porcentaje = Porcentaje
        self.Monto = Monto
        self.NumeroContrato = NumeroContrato
        self.FechaInicio = FechaInicio
        self.FechaFin = FechaFin
        self.PagoUnico = PagoUnico
        
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

class rEmpleadoSueldo(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = "rempleadosueldo"
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, primary_key = True)
    idPuesto = db.Column(db.Integer, primary_key = True)
    Consecutivo = db.Column(db.Integer, primary_key = True)
    Salario = db.Column(db.Numeric(11, 2), nullable = False) 
    Compensacion = db.Column(db.Numeric(11, 2), nullable = False)

    def __init__(self, idPersona, idPuesto, Consecutivo, Salario, Compensacion):
        self.idPersona = idPersona
        self.idPuesto = idPuesto
        self.Consecutivo = Consecutivo
        self.Salario = Salario
        self.Compensacion = Compensacion
    
    # Actualizar Registro
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)