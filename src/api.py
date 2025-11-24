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

@api_bp.route('/viagens/<id_viagem>/paradas')
def get_itinerario(id_viagem):
    sql = text("""
        SELECT
            p.lat_parada,
            p.long_parada,
            p.nome,
            pp.horario_entrada AS horario_chegada
        FROM Passa_por pp
        JOIN Parada p ON pp.id_parada = p.id_parada
        WHERE pp.id_viagem = :id_viagem
        ORDER BY pp.indice_parada ASC
    """)

    try:
        result = db.session.execute(sql, {'id_viagem': id_viagem})

        itinerario = []

        for row in result:
            itinerario.append({
                "lat": float(row.lat_parada),
                "long": float(row.long_parada),
                "nome": row.nome,
                "chegada": str(row.horario_chegada)
            })

        if not itinerario:
            return jsonify({"message": "Viagem not found or has no stops"}), 404

        return jsonify(itinerario)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

