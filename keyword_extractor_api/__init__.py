import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension

# instantiate the extensions
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS", "keyword_extractor_api.config.ProductionConfig")
    app.config.from_object(app_settings)

    # set up extensions
    toolbar.init_app(app)
    bootstrap.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    from keyword_extractor_api.application.health_checks.views import health_check_blueprint
    from keyword_extractor_api.application.rake.views import rake_blueprint

    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(rake_blueprint, url_prefix="/api")

    return app
