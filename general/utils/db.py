from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
#----------------------------------------------------------------------------------------------------------------------
# Creación del objeto SQLAlchemy
db = SQLAlchemy()
# Generación automática de modelos de db
Base = automap_base()
#----------------------------------------------------------------------------------------------------------------------