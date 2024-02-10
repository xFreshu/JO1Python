from app import app, db

# Utworzenie bazy danych
with app.app_context():
    db.create_all()
    print("Baza danych została utworzona.")
