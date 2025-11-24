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
- [ ] Setup do Template
- [ ] Container do Mapa (Leaflet.js + HTML)
- [ ] Interface (Menu select)

### Carlos Felipe (Integracao front + back)
- [ ] Populacao do Dropdown
- [ ] Desenhando a linha (Adicionar um evento de change no dropdown)
- [ ] Plotando as paradas

### Rafael (Backend 1)
- [ ] Endpoint de listagem (`/api/rotas`)
- [ ] Endpoint de tracado (`/api/shape/<id_viagem>`)

### Guilherme (Backend 2)
- [ ] Endpoint de paradas (`/api/paradas/<id_viagem>`)
- [ ] Query JOIN entre as tabelas Viagem, Passa_por, Parada
