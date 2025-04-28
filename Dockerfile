FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
COPY .env .
CMD ["python", "-m", "app.run_analysis_worker"]
