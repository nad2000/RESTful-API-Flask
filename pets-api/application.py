from flask import Flask
from flask_mongoengine import MongoEnine

db = MongoEnine()

def create_app(**config_overrides):

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.config.update(config_overrides)
    db.init_app(app)
    # import blueprints
    from home.views import home_app
    # register blueprints
    app.register_blueprint(home_app)
    return app


