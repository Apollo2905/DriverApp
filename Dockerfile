FROM python:3.12-slim

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000 5025

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]