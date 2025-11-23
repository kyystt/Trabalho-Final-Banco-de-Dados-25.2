#!/bin/bash

user="root"
pass="$MYSQL_ROOT_PASSWORD"
db_name="$MYSQL_DATABASE"

csv_dir="/csv_data"

echo "--- Iniciando a populacao no banco '$db_name' ---"

mariadb -u"$user" -p"$pass" --local-infile=1 "$db_name" << EOF

-- 1. Carregando Agência 
LOAD DATA LOCAL INFILE '$csv_dir/agency.csv'
INTO TABLE \`Agencia\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_agencia, nome);

-- 2. Carregando Parada
LOAD DATA LOCAL INFILE '$csv_dir/stops.csv'
INTO TABLE \`Parada\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_parada, @dummy, nome, lat_parada, long_parada);

-- 3. Carregando Shape
LOAD DATA LOCAL INFILE '$csv_dir/shapes.csv'
INTO TABLE \`Shape\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_shape, indice_ponto, ponto_lat, ponto_long, ponto_dist);

-- 4. Carregando Rota
LOAD DATA LOCAL INFILE '$csv_dir/routes.csv'
INTO TABLE \`Rota\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(id_rota, id_agencia, onibus, nome, @modal_var)
SET modal_rota = IF(@modal_var = 'BRT', TRUE, FALSE);

-- 5. Carregando Viagem
LOAD DATA LOCAL INFILE '$csv_dir/trips.csv'
INTO TABLE \`Viagem\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id_viagem, id_rota, @dummy, destino, @dummy, tipo, id_shape);

-- 6. Carregando Passa_por
LOAD DATA LOCAL INFILE '$csv_dir/stop_times.csv'
INTO TABLE \`Passa_por\`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(id_viagem, indice_parada, id_parada, horario_entrada, horario_saida);

EOF

echo '--- FIM. Todos os dados foram populados. ---';
