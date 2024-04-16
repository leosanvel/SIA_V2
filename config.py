from datetime import timedelta

class Config:
    DEBUG = True
    SECRET_KEY = 'e290235e31eec44eeb4ad58137c42d50'
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:05534DM1N15TR4D0R@localhost/catalogos'
    SQLALCHEMY_BINDS = {
            'db2': 'mysql://root:05534DM1N15TR4D0R@localhost/sia'
        }

    # Desactivar los eventos Flask-SQLALCHEMY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes = 100)
