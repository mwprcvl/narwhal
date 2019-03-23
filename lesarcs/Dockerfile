# use a base image with small OS and small Python installed
ARG base_tag=3.7.2-alpine3.8
FROM python:${base_tag}

WORKDIR /

COPY ./app /app

CMD ["python3", "app/app.py"]
