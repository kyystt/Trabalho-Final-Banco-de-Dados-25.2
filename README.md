# Trabalho Final BD 25.1

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

### Rafael (Backend 1)
* [ ] Endpoint de listagem (`/api/rotas`)
    * Fazer um `SELECT` na tabela Rota e retornar um JSON
* [ ] Endpoint de tracado (`/api/shape/<id_viagem>`)
    * Recebe o `id_viagem`, vai na tabela Shape e seleciona `ponto_lat, ponto_long` e ordena os resultados pelo campo `indice_ponto`

### Guilherme (Backend 2)
* [ ] Endpoint de paradas (`/api/paradas/<id_viagem>`)
* [ ] Query JOIN entre as tabelas Viagem, Passa_por, Parada
    * Retorna um objeto JSON contendo `lat_parada, long_parada, nome (da parada), horario_chegada`
