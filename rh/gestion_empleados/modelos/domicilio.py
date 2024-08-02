from app import db
from catalogos.modelos.modelos import kMunicipio, kEntidad

class rDomicilio(db.Model):
    __tablename__ = "rdomicilio"
    __bind_key__ = 'db2'
    __table_arg__ = {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_spanish_ci"}

    idPersona = db.Column(db.Integer, db.ForeignKey('tpersona.idPersona'), primary_key = True)
    idTipoDomicilio = db.Column(db.Integer, primary_key = True)
    idCP = db.Column(db.Integer, nullable = True)
    idEntidad = db.Column(db.Integer, db.ForeignKey(kEntidad.idEntidad), nullable = True)
    idMunicipio = db.Column(db.Integer, db.ForeignKey(kMunicipio.idMunicipio), nullable = True)
    idLocalidad = db.Column(db.Integer, nullable = True)
    idTipoAsentamiento = db.Column(db.Integer, nullable = True)
    idAsentamiento = db.Column(db.Integer, nullable = True)
    idTipoVialidad = db.Column(db.Integer, nullable = True)
    Vialidad = db.Column(db.String(45), nullable = True)
    NumExterior = db.Column(db.String(45), nullable = True)
    NumInterior = db.Column(db.String(45), nullable = True)
    SinNumero = db.Column(db.Integer, nullable = True)
    DomicilioConocido = db.Column(db.Integer, nullable = True)
    idTipoVialidad01 = db.Column(db.Integer, nullable = True)
    Vialidad01 = db.Column(db.String(45), nullable = True)
    idTipoVialidad02 = db.Column(db.Integer, nullable = True)
    Vialidad02 = db.Column(db.String(45), nullable = True)
    idTipoVialidad03 = db.Column(db.Integer, nullable = True)
    Vialidad03 = db.Column(db.String(45), nullable = True)
    Descripcion = db.Column(db.Text, nullable = True)
    idDomicilio = db.Column(db.Integer, nullable = False)

    # Relacion
    Persona = db.relationship('tPersona', back_populates = "Domicilios", uselist = False, single_parent = True)
    Municipio = db.relationship("kMunicipio", back_populates = "Domicilios", uselist = False, single_parent = True)
    Entidad = db.relationship("kEntidad", back_populates = "Domicilios", uselist = False, single_parent = True)

    def __init__(self, idPersona, idTipoDomicilio, idCP, idEntidad, idMunicipio, idLocalidad, idTipoAsentamiento, idAsentamiento,
                idTipoVialidad, Vialidad, NumExterior, NumInterior, SinNumero, DomicilioConocido, idTipoVialidad01, Vialidad01,
                idTipoVialidad02, Vialidad02, idTipoVialidad03, Vialidad03, Descripcion, idDomicilio):
        self.idPersona = idPersona
        self.idTipoDomicilio = idTipoDomicilio
        self.idCP = idCP
        self.idEntidad = idEntidad
        self.idMunicipio = idMunicipio
        self.idLocalidad = idLocalidad
        self.idTipoAsentamiento = idTipoAsentamiento
        self.idAsentamiento = idAsentamiento
        self.idTipoVialidad = idTipoVialidad
        self.Vialidad = Vialidad
        self.NumExterior = NumExterior
        self.NumInterior = NumInterior
        self.SinNumero = SinNumero
        self.DomicilioConocido = DomicilioConocido
        self.idTipoVialidad01 = idTipoVialidad01
        self.Vialidad01 = Vialidad01
        self.idTipoVialidad02 = idTipoVialidad02
        self.Vialidad02 = Vialidad02
        self.idTipoVialidad03 = idTipoVialidad03
        self.Vialidad03 = Vialidad03
        self.Descripcion = Descripcion
        self.idDomicilio = idDomicilio

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)