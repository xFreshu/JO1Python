from flask import Flask
<<<<<<< HEAD

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
=======
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sekretnyKlucz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Import modeli
from models import User
>>>>>>> 0f5e741 (create basic function which create dblite)
