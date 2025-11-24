# Trabalho Final BD 25.1

## Projeto final da matéria Organização de Dados, do curso de Ciência da Computação da turma 2024.1

## Integrantes
<a href="https://github.com/kyystt/Trabalho-Final-Banco-De-Dados-25.2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=kyystt/Trabalho-Final-Banco-De-Dados-25.2" />
</a>

- Guilherme Vasconcellos Sobreira de Carvalho
- Rafael Mello dos Santos
- Lucas de Moraes Brandão
- Carlos Felipe dos Santos 

## Como comecar a trabalhar?
Primeiro, copie o arquivo `.env.example` para `.env`
```bash
cp .env.example .env
```
E mude tudo que esta escrito com "memude"

Depois basta subir os containers
```bash
docker-compose up
```

## Estrutura do projeto
<details>
<summary>Ver a estrutura de arquivos</summary>

```
.
├── Dockerfile
├── README.md
├── app.py
├── dados
│   ├── agency.csv
│   ├── routes.csv
│   ├── shapes.csv
│   ├── stop_times.csv
│   ├── stops.csv
│   └── trips.csv
├── docker-compose.yml
├── load_data.sh
├── requirements.txt
├── schema.sql
└── src
    ├── __init__.py
    ├── api.py
    ├── config.py
    └── extensions.py
```

</details>

No diretório `dados/` temos todas as populações das nossas tabelas em arquivos `csv`, que é usado no script `load_data.sh`

Em `src/`, temos a configuração do nosso banco de dados (e o arquivo de configuração) e a API

`app.py` é o resto da aplicação, que serve algumas páginas estáticas como `/health`

## A fazer 
### Lucas (Frontend)
* Setup do Template
    * [ ] Criar uma pasta templates na raiz do projeto (`/`) e um arquivo `index.html`
    * [ ] Configurar o flask no `app.py` para renderizar esse template na rota 
* Container do Mapa (Leaflet.js + HTML)
    * [ ] Criar uma div onde o mapa vai renderizar
    * [ ] Centralizar a visualizacao inicial nas coordenadas do Rio de Janeiro
* Interface (Menu select)
    * [ ] Criar um menu dropdown onde futuramente aparecerao os nomes das linhas de onibus

### Carlos Felipe (Integracao front + back)
* [ ] Populacao do Dropdown
    * [ ] Escrever um script JS no `index.html` que, ao carregar a pagina, faz um `fetch('/api/rotas')` e cria as `<option>` dentro do dropdown
* [ ] Desenhando a linha (Adicionar um evento de change no dropdown)
    * Quando o usuario escolher uma linha, o JS deve limpar o mapa, chamar `/api/shape/...` e usar a funcao `L.polyline` do Leaflet para desenhar o trajeto colorido
* [ ] Plotando as paradas
    * No mesmo evento, deve chamar `/api/paradas/...` e usar um loop para adicionar `L.marker` no mapa para cada parada retornada
* [ ] Contar quantas rotas cada agência opera, ordenando do maior para a menor 
    * Agregacao (COUNT) + GROUP BY
* [ ] Calcular quantos pontos de GPS (linhas na tabela Shape) cada viagem possui 
    * Agregacao (COUNT) + GROUP BY
* [ ] Média global de paradas por viagem 
    * Agregacao (AVG)

### Rafael (Backend 1)
* [ ] Endpoint de listagem (`/api/rotas`)
    * Fazer um `SELECT` na tabela Rota e retornar um JSON
* [ ] Endpoint de tracado (`/api/shape/<id_viagem>`)
    * Recebe o `id_viagem`, vai na tabela Shape e seleciona `ponto_lat, ponto_long` e ordena os resultados pelo campo `indice_ponto`
* [ ] Listar apenas as rotas que passam por uma parada especifica famosa (ex.: "Candelária") 
    * Subconsulta Simples
* [ ] Listar as viagens que têm um número de paradas acima da média 
    * Subconsulta com Agragacao
* [ ] Listar as Agências que operam apenas ônibus do tipo "BRT" (`modal_rota = true`)

### Guilherme (Backend 2)
* [ ] Endpoint de paradas (`/api/paradas/<id_viagem>`)
* [ ] Query `JOIN` entre as tabelas Viagem, Passa_por, Parada
    * Retorna um objeto JSON contendo `lat_parada, long_parada, nome (da parada), horario_chegada`
* [ ] Recuperar `nome (da agencia), nome (da rota), destino da viagem, nome (da parada final)` 
    * Mostrar detalhes da viagem quando o usuário clica num ônibus
    * JOIN
* [ ] Listar todas as paradas de uma Viagem específica
    * JOIN
* [ ] Obter as coordenadas (`lat/long`) para desenhar o Shape 
    * JOIN
* [ ] Listar todas as Agências cadastradas, inclusive as que nao possuem nenhuma rota ativa 
    * LEFT JOIN
