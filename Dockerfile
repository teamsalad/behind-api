FROM python:3.7-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install pipenv
RUN pip3 install pipenv

# Set working directory and copy Pipfiles
WORKDIR /app/src
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install application dependencies
RUN apk add --no-cache --virtual .build-deps \
      mariadb-dev build-base openssl-dev libffi-dev musl-dev linux-headers && \
      pipenv install --deploy --system && \
      apk add --virtual .runtime-deps mariadb-client py-mysqldb && \
      apk del .build-deps

COPY . .

EXPOSE 8000

CMD ["python", "behind/manage.py", "runserver", "0.0.0.0:8000"]

