from models import AdminUser
from main import app, db

with app.app_context():
    db.create_all()
    # create an admin user
    AdminUser.create_admin('Ali5', 'passphrase')
    AdminUser.create_admin('Simpan', 'passphrase')
