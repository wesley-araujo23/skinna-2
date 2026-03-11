from flask import Flask
from skinna.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skinna.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "minha_chave_secreta"  # use SECRET_KEY, não secret_key

db.init_app(app)

from skinna import routes