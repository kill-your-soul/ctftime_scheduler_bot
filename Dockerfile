FROM python:3.10 as builder

WORKDIR /builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /builder/wheels -r requirements.txt

FROM python:3.10-slim-buster

WORKDIR /app
COPY . .
RUN apt-get update
COPY --from=builder /builder/wheels /app/wheels
COPY --from=builder /builder/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache /app/wheels/*
ENTRYPOINT [ "python", "ctftime_sch/main.py" ]