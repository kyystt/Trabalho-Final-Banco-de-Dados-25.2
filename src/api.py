from flask import Blueprint, jsonify
from sqlalchemy import text

# DB from project
from src.extensions import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/paradas/<id_parada>')
def get_parada(id_parada):
    sql = text("SELECT * FROM Parada WHERE id_parada = :id")
    result = db.session.execute(sql, {'id': id_parada})

    paradas_list = [dict(row._mapping) for row in result]

    if paradas_list:
        return jsonify(paradas_list)
    else:
        return jsonify({"error": "Parada not found"}), 404

@api_bp.route('viagens/<id_viagem>')
def get_viagem_detalhes(id_viagem):
    sql = text("""
        SELECT
            A.nome AS nome_agencia,
            R.nome AS nome_rota,
            R.onibus AS numero_linha,
            V.destino AS letreiro_destino,
            P.nome AS nome_ponto_final
        FROM Viagem V
        JOIN Rota R on V.id_rota = R.id_rota
        JOIN Agencia A ON R.id_agencia = A.id_agencia
        JOIN Passa_por PP on V.id_viagem = PP.id_viagem
        JOIN Parada P on PP.id_parada = P.id_parada
        WHERE V.id_viagem = :id
        ORDER BY PP.indice_parada DESC
        LIMIT 1
    """)

    try:
        result = db.session.execute(sql, {"id": id_viagem})

        row = result.fetchone()

        if not row:
            return jsonify({"error": "Viagem not found"}), 404

        data = dict(row._mapping)

        return jsonify({
            "agencia": data['nome_agencia'],
            "rota": f"{data['numero_linha']} - {data['nome_rota']}",
            "destino" : {
                "letreiro": data['letreiro_destino'],
                "ponto_final": data['nome_ponto_final']
            }
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500

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
        WHERE pp.id_viagem = :id
        ORDER BY pp.indice_parada ASC
    """)

    try:
        result = db.session.execute(sql, {'id': id_viagem})

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

@api_bp.route('/rotas/<id_rota>/shapes')
def get_shape_by_route(id_rota):
    sql = text("""
        SELECT DISTINCT
            S.id_shape,
            S.ponto_lat, 
            S.ponto_long,
            S.indice_ponto
        FROM Viagem V
        JOIN Rota R ON V.id_rota = R.id_rota
        JOIN Shape S ON V.id_shape = S.id_shape
        WHERE R.id_rota = :id
        ORDER BY S.id_shape, S.indice_ponto ASC
    """)
    
    try: 
        result = db.session.execute(sql, {'id': id_rota})

        shapes = {}

        for row in result:
            shape_id = row.id_shape
            if shape_id not in shapes:
                shapes[shape_id] = []

            shapes[shape_id].append({
                "lat": float(row.ponto_lat),
                "long": float(row.ponto_long),
            })

        if not shapes:
            return jsonify({"message":"Shapes not found"}), 404

        return jsonify(shapes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('agencias')
def get_agencias_overview():
    sql = text("""
        SELECT 
            A.id_agencia,
            A.nome,
            COUNT(R.id_rota) as total_rotas
        FROM Agencia A
        LEFT JOIN Rota R ON A.id_agencia = R.id_agencia
        GROUP BY A.id_agencia, A.nome
        ORDER BY total_rotas DESC
    """)

    try:
        result = db.session.execute(sql)

        agencias = []

        for row in result:
            agencias.append({
                "id": row.id_agencia,
                "nome": row.nome,
                "rotas_ativas": row.total_rotas
            })

        if not agencias:
            return jsonify({"message": "Agencias not found"}), 404

        return jsonify(agencias)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
