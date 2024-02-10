from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'tajny_klucz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja bazy danych
db = SQLAlchemy(app)

# Inicjalizacja Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nazwa funkcji widoku logowania

# Model użytkownika
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importowanie tras
from routes import setup_routes
setup_routes(app)

# Ścieżka do pliku CSV
file_path = 'ścieżka_do_twojego_pliku.csv'  # Zmień na rzeczywistą ścieżkę do pliku

if __name__ == '__main__':
    app.run(debug=True)
