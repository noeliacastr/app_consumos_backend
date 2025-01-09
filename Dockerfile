FROM python:3.11.2

# Instala las dependencias del sistema para pyodbc
RUN apt-get update && \
    apt-get install -y unixodbc-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]