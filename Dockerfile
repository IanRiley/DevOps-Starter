FROM python:3.10 as base

WORKDIR /

RUN pip install poetry

COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry install

#RUN pip install gunicorn
#RUN pip install flask

COPY . .

FROM base as dev
ENV FLASK_ENV=dev
RUN pip install flask
ENTRYPOINT [ "poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5001" ]
EXPOSE 5001

FROM base as prod
ENV FLASK_ENV=prod
RUN pip install gunicorn
ENTRYPOINT [ "poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "todo_app.app:create_app()" ]
EXPOSE 5000

FROM base as test
ENV FLASK_ENV=test
ENTRYPOINT [ "poetry", "run", "pytest" ]
EXPOSE 5000