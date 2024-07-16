FROM python:3.11-slim-buster

WORKDIR /app

COPY Pipfile* /app/

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY app/ /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
