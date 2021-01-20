FROM python:3.7-slim-buster

# Setting workdir
WORKDIR /forecast_api

# Update OS and install Python
RUN apt-get update && \
    apt-get install -y git python3-dev && \
    pip3 install --upgrade pip

# Install requirements
COPY "requirements.txt" ./
RUN python3.7 -m pip install -r requirements.txt

# Copy project to workdir
COPY ["app.py", "./"]

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]