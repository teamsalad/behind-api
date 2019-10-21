FROM python:3.7-alpine AS base
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYROOT /pyroot
ENV PATH $PYROOT/bin:$PATH
ENV PYTHONUSERBASE $PYROOT

FROM base AS builder
# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN apk add --no-cache --virtual .build-deps \
      mariadb-dev build-base openssl-dev libffi-dev musl-dev linux-headers && \
      PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --deploy --system && \
      apk del .build-deps

FROM base
RUN apk add --virtual .runtime-deps mariadb-client py-mysqldb
WORKDIR /app/src
COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY --from=builder $PYROOT/bin/ $PYROOT/bin/
COPY . .

EXPOSE 8000

CMD ["python", "behind/manage.py", "runserver", "0.0.0.0:8000"]
