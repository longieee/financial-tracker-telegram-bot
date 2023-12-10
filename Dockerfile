FROM python:3.11.7-bullseye

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/* /app/

ENTRYPOINT ["python", "main.py"]