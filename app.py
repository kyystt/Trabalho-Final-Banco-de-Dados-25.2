from flask import Flask
from src import db
from src import api_bp
from src import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def index():
        return '<p> OIIII </p>'

    @app.route("/health")
    def health():
        return 'SHALL THERE BE LIGHT!', 200

    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
