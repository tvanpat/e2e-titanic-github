FROM tiangolo/uvicorn-gunicorn-fastapi:latest-2020-06-06

ENV PYTHONUNBUFFERED 1 

COPY ./src/setup.py /usr/src
WORKDIR /usr/src
RUN pip install .

COPY ./src/app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]