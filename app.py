from flask import Flask, render_template
from src import db, api_bp, Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return 'SHALL THERE BE LIGHT!', 200

    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
