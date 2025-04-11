# app/__init__.py
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from .config import Config
from dotenv import load_dotenv

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    load_dotenv()  # ✅ Load environment variables from .env
    print(">>> Calling create_app()")

    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # ✅ Register blueprints
    from .auth import auth_bp
    from .generate import generate_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(generate_bp, url_prefix="/generate")

    # ✅ Add homepage route here (after app is defined)
    @app.route('/')
    def index():
        return render_template("index.html")

    return app
