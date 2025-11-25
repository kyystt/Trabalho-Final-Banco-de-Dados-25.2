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

@api_bp.route('rotas/principais')
def get_rotas_principais():

    sql = text("""
        WITH StatsViagem AS (
            SELECT id_viagem, COUNT(id_parada) as qtd
            FROM Passa_por
            GROUP BY id_viagem
        ),
        MediaGlobal AS (
            SELECT AVG(qtd) as valor_medio FROM StatsViagem
        )
        
        SELECT 
            r.onibus,
            r.nome as nome_rota,
            CAST(AVG(sv.qtd) AS UNSIGNED) as media_paradas_rota
        FROM Rota r
        JOIN Viagem v ON r.id_rota = v.id_rota
        JOIN StatsViagem sv ON v.id_viagem = sv.id_viagem
        GROUP BY r.id_rota, r.onibus, r.nome
        HAVING media_paradas_rota > (SELECT valor_medio FROM MediaGlobal)
        ORDER BY media_paradas_rota DESC
        LIMIT 100;
    """)

    try:
        result = db.session.execute(sql)
        
        rotas_longas = []

        for row in result:
            rotas_longas.append({
                "linha": row.onibus,           
                "nome_rota": row.nome_rota,    
                "media_paradas": row.media_paradas_rota
            })

        if not rotas_longas:
            return jsonify({"message": "Nenhuma rota encontrada acima da média"}), 404

        return jsonify(rotas_longas)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@api_bp.route('rotas/<id_parada>')
def get_rota_by_parada(id_parada):
    sql = text("""SELECT * 
               FROM Rota R
               WHERE R.id_rota IN (
                    SELECT 
                        V.id_rota 
                    FROM Viagem V 
                    WHERE V.id_viagem IN (
                        SELECT P.id_viagem 
                        FROM Passa_por P 
                        WHERE P.id_parada = :id))
    """)

    try:
        result = db.session.execute(sql,{'id': id_parada})

        rotas = []

        for row in result:

            rotas.append({
                "id": row.id_rota,
                "nome": row.nome,
                "numero": row.onibus,
                "id_agencia": row.id_agencia,
                "is_brt": bool(row.modal_rota)
            })

        if not rotas:
            return jsonify({"message": "Parada not found"}), 404

        return jsonify(rotas)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('shape/<id_viagem>')
def get_shape_by_viagem(id_viagem):
    sql = text("""SELECT
                    S.id_shape, 
                    S.ponto_lat,
                    S.ponto_long,
                    S.indice_ponto
               FROM Shape S
               JOIN Viagem V ON V.id_shape = S.id_shape
               WHERE V.id_viagem = :id
               ORDER BY S.id_shape, S.indice_ponto ASC
               """)

    try:
        result = db.session.execute(sql,{'id': id_viagem})

        pontos = []

        for row in result:

            pontos.append({
                "lat": float(row.ponto_lat),
                "long": float(row.ponto_long),
            })

        if not pontos:
            return jsonify({"message": "Shape not found"}), 404

        return jsonify(pontos)

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
    
@api_bp.route('rotas')
def get_rotas_overview():
    sql = text("SELECT * FROM Rota")

    try:
        result = db.session.execute(sql)

        rotas = []

        for row in result:
            rotas.append({
                "id": row.id_rota,
                "nome": row.nome,
                "numero": row.onibus,
                "id_agencia": row.id_agencia,
                "is_brt": bool(row.modal_rota)
            })

        if not rotas:
            return jsonify({"message": "Rotas not found"}), 404

        return jsonify(rotas)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_bp.route('/viagens/<id_viagem>/pontos_shape_count')
def get_viagens_pontos_shape_count(id_viagem):
    sql = text("""
        SELECT 
            V.id_viagem,
            COUNT(S.id_shape) AS total_pontos_gps
        FROM Viagem V
        LEFT JOIN Shape S ON V.id_shape = S.id_shape
        WHERE V.id_viagem = :id
        GROUP BY V.id_viagem
    """)

    try:
        result = db.session.execute(sql, {'id': id_viagem})
        row = result.fetchone()

        if not row:
            return jsonify({"message": "Viagem not found"}), 404

        return jsonify({
            "id_viagem": row.id_viagem,
            "total_pontos_gps": int(row.total_pontos_gps)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_bp.route('/viagens/media_paradas')
def get_media_paradas_por_viagem():
    sql = text("""
        SELECT AVG(cnt) AS media_paradas FROM (
            SELECT COUNT(*) AS cnt
            FROM Passa_por
            GROUP BY id_viagem
        ) AS sub
    """)
    try:
        result = db.session.execute(sql)
        row = result.fetchone()
        media = float(row.media_paradas) if row and row.media_paradas is not None else 0.0
        return jsonify({"media_paradas_por_viagem": round(media, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_bp.route('/rotas/<id_rota>/paradas')
def get_paradas_by_rota(id_rota):
    sql = text("""
        SELECT
            v.id_shape,
            p.id_parada,
            p.nome,
            p.lat_parada,
            p.long_parada,
            MIN(pp.indice_parada) AS primeiro_indice
        FROM Parada p
        JOIN Passa_por pp ON p.id_parada = pp.id_parada
        JOIN Viagem v ON pp.id_viagem = v.id_viagem
        WHERE v.id_rota = :id
        GROUP BY v.id_shape, p.id_parada, p.nome, p.lat_parada, p.long_parada
        ORDER BY v.id_shape, primeiro_indice ASC
    """)
    try:
        result = db.session.execute(sql, {'id': id_rota})

        paradas_por_shape = {}

        for row in result:
            shape_id = row.id_shape
            if shape_id not in paradas_por_shape:
                paradas_por_shape[shape_id] = []

            paradas_por_shape[shape_id].append({
                "id_parada": row.id_parada,
                "nome": row.nome,
                "lat": float(row.lat_parada),
                "long": float(row.long_parada),
                "primeiro_indice": int(row.primeiro_indice)
            })

        if not paradas_por_shape:
            return jsonify({"message": "Nenhuma parada encontrada para essa rota"}), 404

        return jsonify(paradas_por_shape)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/rotas/<id_rota>/viagens')
def get_viagens_da_rota(id_rota):
    sql = text("""
        SELECT
            id_viagem,
            id_shape
        FROM Viagem
        WHERE id_rota = :id
    """)
    result = db.session.execute(sql, {'id': id_rota})

    viagens = []
    for row in result:
        viagens.append({
            "id_viagem": row.id_viagem,
            "id_shape": row.id_shape
        })

    return jsonify(viagens)