# scheduling_app/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object('scheduling_app.config.TestingConfig')
    else:
        app.config.from_object('scheduling_app.config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from scheduling_app.api import api_bp
    from scheduling_app.auth import auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/')
    def home():
        return {'message': 'Welcome to the scheduling system'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=True)
