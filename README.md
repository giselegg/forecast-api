# Weather Forecast API

API para consultar a previsão do tempo, filtrando por cidade, para 7 dias.

## Requerimentos

- Python 3.7+
- Libs: requirements.txt

## Como usar
### 1 Baixar projeto
```
git clone https://github.com/giselegg/forecast-api
```

### 2a Com Docker
- Criar o container:
```
docker build -t forecast-api .
```

- Subir o container:
```
docker run -p 8000:8000 forecast-api
```

### 2b Sem Docker
- Criar ambiente virtual:
```
python3 -m venv env
```

- Ativá-lo:
```
source env/bin/activate
```

- Instalar Requirements:
```
pip install -r requirements.txt
```

- Rodar API:
```
uvicorn app:app
```

### 3 Testar saúde da API
Para testar a saúde da API, fazendo a seguinte requisição deve retornar o timestamp da mesma.

```
[GET] http://localhost:8000/health
```

## That's all folks!