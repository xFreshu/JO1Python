import pandas as pd
import bcrypt
import json
from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm, RegistrationForm
from models import User, db
from flask_login import login_user, login_required, logout_user


# konfiguracja ścieżek
def setup_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
                login_user(user)
                return redirect(url_for('app'))
            else:
                flash('Invalid username or password')
        return render_template('login.html', form=form)

# Rejestracja użytkownika
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

# Strona główna aplikacji
    @app.route('/')
    def index():
        return render_template('index.html')

# Wylogowanie użytkownika
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # Ścieżka do pliku CSV
    file_path = 'Ofiary zabójstw 2013-2022.csv'  # Zmień na rzeczywistą ścieżkę do pliku

    def load_and_process_data(file_path):
        data = pd.read_csv(file_path, sep=';')
        # Sumowanie ofiar rok do roku
        yearly_victims = data.groupby('rok')['wartosc'].sum().reset_index()
        # Sumowanie ofiar według grup wiekowych
        age_group_victims = data.groupby('grupy_wieku')['wartosc'].sum().reset_index()
        return yearly_victims['rok'].tolist(), yearly_victims['wartosc'].tolist(), age_group_victims[
            'grupy_wieku'].tolist(), age_group_victims['wartosc'].tolist()

    # Ścieżka do głównej ścieżki aplikacji z wykresami
    @app.route('/application')
    @login_required
    def app():
        years, victims, age_groups, age_group_victims = load_and_process_data(file_path)
        data = {
            "years": years,
            "victims": victims,
            "ageGroups": age_groups,
            "ageGroupVictims": age_group_victims
        }
        return render_template('app.html', data=json.dumps(data))