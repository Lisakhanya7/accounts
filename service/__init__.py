import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman

from service.routes import api


def create_app():
    app = Flask(__name__)

    # Set ALLOW_ALL_ORIGINS=true only for local coursework demonstrations.
    allowed_origin = os.getenv("CORS_ORIGIN", "http://localhost:3000")
    CORS(app, resources={r"/*": {"origins": [allowed_origin]}})

    # HTTPS is disabled for local HTTP/container demonstrations. Enable it
    # behind HTTPS in a production deployment.
    Talisman(
        app,
        force_https=os.getenv("FORCE_HTTPS", "false").lower() == "true",
        content_security_policy={
            "default-src": ["'self'"],
            "style-src": ["'self'", "'unsafe-inline'"],
            "script-src": ["'self'"],
        },
    )

    app.register_blueprint(api)

    @app.get("/")
    def index():
        return jsonify({"application": "accounts", "status": "running"}), 200

    return app


app = create_app()

__all__ = ["app", "create_app"]
