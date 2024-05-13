FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "4484", "main:app" ]
EXPOSE 4484