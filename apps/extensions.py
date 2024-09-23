"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

# login_manager = LoginManager()
db = SQLAlchemy()
moment = Moment()
