from flask import Flask  # Importing the Flask class
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy for database operations
from os import path  # Importing the path module from os for file path operations
from flask_login import LoginManager  # Importing LoginManager for user session management

db = SQLAlchemy()  # Creating an instance of SQLAlchemy
DB_NAME = "database.db"  # Setting the name of the SQLite database file


def create_app():
    app = Flask(__name__)  # Creating an instance of the Flask application
    app.config['SECRET_KEY'] = 'signing cookies for security'  # Setting the secret key for the Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Setting the database(Uniform Resource Identifier) for SQLAlchemy
    db.init_app(app)  #  initializes the SQLAlchemy extension with the Flask application.

    from .views import views  # Importing the views blueprint
    from .auth import auth  # Importing the auth blueprint

    # modular components and define namespaces
    app.register_blueprint(views, url_prefix='/')  # Registers the views blueprint with the Flask application
    app.register_blueprint(auth, url_prefix='/')  # Registers the auth blueprint with the Flask application

    from .models import User, Note  # These models define the structure of the database tables.

    with app.app_context():
        db.create_all()  # Creating all database tables defined in the models

    login_manager = LoginManager()  # Creating an instance of LoginManager
    login_manager.login_view = 'auth.login'  # Setting the login view for LoginManager
    login_manager.init_app(app)  # Initializing LoginManager with the Flask app

    @login_manager.user_loader # This line is a decorator for the function load_user, which loads a user from the database based on the user's ID.
    def load_user(id):
        return User.query.get(int(id))  # Loading a user by ID using the User model

    return app  # Returning the Flask app instance


def create_database(app):
    if not path.exists('website/' + DB_NAME):  # Checking if the database file exists
        db.create_all(app=app)  # Creating all database tables if the file doesn't exist
        print('Created Database!')  # Printing a message indicating that the database was created
