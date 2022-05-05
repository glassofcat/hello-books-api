from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os #reads env variables

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() #loads .env for os to see

def create_app(test_config=None):
    
    # app.config['']
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.book import Book

    # db.init_app(app)
    # migrate.init_app(app, db)
    
    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app