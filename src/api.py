from flask import Blueprint, jsonify
from sqlalchemy import text

# DB from project
from src.extensions import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/agencias')
def get_agencias():
    try:
        sql = text("SELECT * FROM Agencia LIMIT 5")
        result = db.session.execute(sql)

        agencias_list = [dict(row._mapping) for row in result]

        return jsonify({
            "status": "success",
            "message": "foi!",
            "data": agencias_list
        })

    except Exception as e:
        return jsonify({ "status": "error", "message":str(e) }), 500

@api_bp.route('/paradas/<id>')
def get_parada(id):
    sql = text("SELECT * FROM Parada WHERE id_parada = :id")
    result = db.session.execute(sql, {'id': id})
    
    paradas_list = [dict(row._mapping) for row in result]

    if paradas_list:
        return jsonify(paradas_list)
    else:
        return jsonify({"error": "Parada not found"}), 404
