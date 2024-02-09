from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm, RegistrationForm
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import bcrypt


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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/application')
    @login_required
    def app():
        return render_template('app.html', title='Jezyki Obiektowe 1 - Semestr 1')
