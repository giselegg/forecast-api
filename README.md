# Weather Forecast API

API para consultar a previsão do tempo, filtrando por cidade, para 7 dias.

## Requerimentos

- Python 3.8.5
- Libs: requirements.txt

- Criar uma chave na HG Weather para consulta pública:
https://console.hgbrasil.com/keys

## Como usar
### 1 Baixar projeto
```
git clone https://github.com/giselegg/forecast-api
```

### 2 Chave da API da HG Weather
Salvar a chave num arquivo .env na variável KEY

### 3a Com Docker
- Criar o container:
```
docker build -t forecast-api .
```

- Subir o container:
```
docker run -p 8000:8000 forecast-api
```

### 3b Sem Docker
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

### 4 Testar saúde da API
Para testar a saúde da API, fazendo a seguinte requisição deve retornar o timestamp da mesma.

```
[GET] http://localhost:8000/health
```

### 5 Consulta de previsão do tempo
```
[GET] http://localhost:8000/forecast/<city_name>
```

### 6 CRUD usuários

**Retornar todos os usuários**
```
[GET] http://localhost:8000/users/
```

**Adicionar usuário**

Enviar JSON com:
```
{
    "username": <nome_usuario>,
    "password": <senha>,
}
```
para:
```
[POST] http://localhost:8000/users/
```

**Remover usuário**
```
[DELETE] http://localhost:8000/users/<id>
```

**Atualizar usuário**

Enviar JSON com:
```
{
    "username": <nome_usuario>,
    "password": <senha>,
}
```
para:
```
[PUT] http://localhost:8000/users/<id>
```

## Testes unitários
```
python3 -m pytest
```

## Fonte
**[API Externa] HG Weather**
https://hgbrasil.com/status/weather

## That's all folks!
