FROM python:3.8.5-alpine3.12

RUN apk update && apk add --no-cache \
        gcc \
        ca-certificates \
        libxslt \
        libxml2 \
        libressl \
        libffi \
        py-gunicorn \
        postgresql-libs \
        postgresql-client
RUN pip install --upgrade pip==19.0.2 && \
    pip install pipenv

WORKDIR /app
COPY Pipfile* /app/

RUN apk add --no-cache --virtual .build-deps \
        g++ \
        build-base \
        make \
        linux-headers \
        python3-dev \
        musl-dev \
        postgresql-dev \
        libressl-dev \
        libxslt-dev \
        libffi-dev && \
    pipenv install --system --deploy --dev -v && \
    apk del .build-deps

COPY . /app/
ENV PORT=8080
EXPOSE 8080

CMD [ "gunicorn", "{{cookiecutter.project_slug}}.app:create_app()", "-b", "0.0.0.0:8080", "--access-logfile", "-", "--access-logformat", "%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""]
