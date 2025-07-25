FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY backend/app app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
