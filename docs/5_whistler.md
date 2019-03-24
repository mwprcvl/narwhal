# Getting started with Docker and Rstudio

## Purpose

I wanted to document my attempt to integrate Rstudio with Docker to improve the reproducibility of my work in different environments.

## Prerequisites

The following text assumes Docker is installed.

## Dockerfile

A variety of Docker images are available for R. I choose to work with `rocker/verse` when image size doesn't matter because it is the most comprehensive.

```
ARG base_tag="3.5.2"
FROM rocker/verse:${base_tag}
```

I add packages to this image to reflect my needs. The Dockerfile should reflect versions of additional packages, which is accomplished within R by using devtools::install_version

```
RUN Rscript -e 'devtools::install_version("plotly", version = "4.8.0", repos = "http://cran.us.r-project.org")' && \
  Rscript -e 'devtools::install_version("caret", version = "6.0-81", upgrade = "never", repos = "http://cran.us.r-project.org")' && \
  Rscript -e 'devtools::install_version("xgboost", version = "0.81.0.1", upgrade = "never", repos = "http://cran.us.r-project.org")'
```

For the sake of simplicity, I set the working directory to be the user home directory. This will make mounting and launch of Rstudio Server simpler later on.

```
WORKDIR /home/rstudio
```

## Compose

I will run this service using a `docker-compose` configuration. The environment variables I have noted here for reference are `PASSWORD`, which sets the login password for the user `rstudio` on the server. Using a different port for publication and target reflects my use case of many images running simultaneously. The volume bind here means that local code is accessible to the remote container, and deliberately allows the R session itself to be stateful if I restart the container.

```
version: '3.6'
services:
  rs:
    build:
      args:
        base_tag: "3.5.2"
      context: .
    environment:
      - PASSWORD=abc123
    image: whistler:latest
    ports:
      -
        published: 18787
        target: 8787
    tty: true
    volumes:
      -
        type: bind
        source: ./r
        target: /home/rstudio
```

## Launch

Simply running `docker-compose up -d` starts the container. Then go to `${DOCKER_IP}:18787` in a browser to start an Rstudio session. `${DOCKER_IP}` is either `localhost` or the VM's IP address.

## Summary


