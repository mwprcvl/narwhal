# Getting started with Anaconda on Docker

## Purpose

I wanted to set up an Anaconda Python environment on a Docker container. This would be a starting point for a project that could be developed on a laptop and scaled on a server. This information is also captured in a working example [here](../saasfee).

## Prerequisites

The following text assumes Docker is installed and familiarity with `docker-compose`.

## A `conda` environment on a container

The `Dockerfile` is using the Miniconda base image, and creating a conda environment from an  `environment.yml` file. After install, there is some cleanup to reduce the resulting image size.

```docker
ARG base_tag=4.5.12
FROM continuumio/miniconda3:${base_tag}
COPY environment.yml .
RUN /opt/conda/bin/conda env create --file environment.yml && \
  /opt/conda/bin/conda clean -tipsy
```

```yml
name: saasfee
dependencies:
  - python=3.7
  - jupyter
  - pandas=0.24
  - psycopg2=2.7
  - sqlalchemy=1.2
  - scikit-learn=0.20
```

## A non-root user for the container

Best practice is to run the container as a non-root user. In the `Dockerfile` I add a user with other settings for login, using a common pattern.

```docker
ARG conda_user=appuser
ARG conda_home=/app
RUN set -eux; \
  groupadd -r ${conda_user} --gid=999; \
  useradd -r -g ${conda_user} --uid=999 --home-dir=${conda_home} \
    --shell=/bin/bash ${conda_user}; \
  mkdir -p ${conda_home}; \
  chown -R ${conda_user}:${conda_user} ${conda_home}
```

Within the compose file, I then give appropriate build arguments to set up the non-root user.

```yml
build:
  args:
    base_tag: 4.5.12
    conda_user: appuser
    conda_home: /appuser
    context: .
```

## Activate the `conda` environment

In order for the application to use the virtual environment, there are a couple of tricks to getting it activated. Firstly, the `Dockerfile` should modify `.bashrc` for the non-root user.

```docker
ENV USER=${conda_user}
USER ${USER}
WORKDIR ${conda_home}
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate saasfee" >> ~/.bashrc
```

Secondly, the Compose YAML should invoke an interactive shell when launching Jupyter to use the environment.

```yml
command: bash -ic 'jupyter notebook --notebook-dir=/py_notebooks --no-browser --ip=0.0.0.0'
```

Thirdly, any non-login program should first `source .bashrc` so that the `conda` environment is activated.

## Using `jupyter`

The Compose YAML should set a password for Jupyter for login from the browser, and map a port from the host (published) to the container (target).

```yml
  environment:
    - JUPYTER_TOKEN=abc123
  ports:
    -
      published: 1888
      target: 8888
```

The Jupyter notebook is then accessible at `<docker_ip>:18888/` using the password `abc123`.

## Making locally editable code available to the container

I bind two local directories in the project, one for source code and one for Jupyter notebooks, so that I can modify code locally to run in the container.

```yml
volumes:
  -
    type: bind
    source: ./py_notebooks
    target: /py_notebooks
```

## Using an explicit environment file

Initially I gave only approximate versions for the packages I wanted in my `conda` environment, and I let `conda` resolve the exact builds. For future reproducibility, I generate an explicit YAML file so that the next build will be identical. Create this file in Terminal and modify the `Dockerfile`.

```sh
docker-compose up -d
docker exec -it saasfee_py_1 bash -ic "conda list --explicit" > explicit.yml
docker-compose down
```

```docker
COPY ./py_notebooks/explicit.yml environment.yml
```

## Summary

I have demonstrated the use of the Miniconda base image to launch a custom Python environment. I have shown how to configure non-root user accounts for use with Jupyter. I also showed how to bind volumes so that code on a container can be modified locally.
