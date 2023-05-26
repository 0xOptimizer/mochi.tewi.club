from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from importlib import import_module
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure email settings
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
)

app.DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL')

mail = Mail(app)

blueprint_names = [
    'main',
    'api_key',
    'breed_scanner',
]

# Import and register Blueprints
for blueprint_name in blueprint_names:
    blueprint_module = import_module(f'.routes.{blueprint_name}', package=__package__)
    blueprint = getattr(blueprint_module, f'{blueprint_name}_bp')
    app.register_blueprint(blueprint)