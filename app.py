import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL')

if not db_url:
    exit()

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def check_connection():
    try:
        sql = text("SELECT * FROM Agencia LIMIT 5")
        result = db.session.execute(sql)

        agencies = []
        for row in result:
            agencies.append(dict(row._mapping))

        return jsonify({
            "status": "success",
            "message": "CONECTADO PORRA",
            "data": agencies
        })

    except Exception as e:
        return jsonify({ "status": "error", "message":str(e) }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
