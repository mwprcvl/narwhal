# Getting started with Docker

## Purpose

I wanted to document some of the things I have learned about Docker, particularly the nuances of some of the commands. This information is also captured in a working example [here](../valthorens/).

## Prerequisites

The following text assumes Docker is installed. If you are using `boot2docker`, e.g., Docker is not running natively but on VirtualBox, start the VM with `docker-machine`.

```sh
docker-machine ip default
```

Then make sure the environment variables are exported to the Terminal so that Docker commands can be used.

```sh
eval "$(docker-machine env default)"
```

Note that with the native Docker, the appropriate IP is localhost, but with the non-native environment, it will be the VM IP, often `192.168.99.100`, or given by the following command.

```sh
docker-machine ip default
```

## Essential concepts

In order to make sense of what follows, there are some concepts that first must be understood. These are taken from the writeup [here](https://vsupalov.com/6-docker-basics/).

* container: instance of an image; a running machine
* image: snapshot of a machine state; a powered off machine
  * don't rely on defaults when you boot the image
  * set variables to work in your host as it suits you
* `Dockerfile`: instructions for creating an image
* volume: a way to get data from a container to persist into a new container
* port forwarding: app listens on one port, Docker exposes another
  * application has a port, say 5000
  * Docker exposes another port on server for this, say 9010, for local apps
* `docker-compose`: a tool for avoiding long docker commands
  * it uses a YAML file for structuring arguments

## Basic operations

First define some variables to make the commands a little clearer. Let us assume we are creating and image, with the name stored in `image_name` and its version stored in `image_version`, and a container, with its name stored in `container_name`. Also, we assume that a `Dockerfile` exists in the current directory.

```sh
image_name=valthorens
image_version=0.1
container_name=caron
```

To build an image from the `Dockerfile`, we use the `build` command with `--rm` option to avoid building up a lot of intermediate images, we use the `-t` option to tag the image with a meaningful name.

```sh
docker build --rm -t ${image_name} .
```

Assuming that `docker build` runs successfully, an image will be created. We can then create a container from the image using the `run` command, with the `-t` option for rendering the terminal output and the `-i` option for interactive mode. The console will return whatever the entrypoint defines, but more on that later. Exit the console to stop the container. The `--rm` option will remove the container when the (default) command exits, which is helpful if you are doing a lot of `docker run...`.

```sh
docker run --rm  -i -t --name ${container_name} ${image_name}
```

To tag the image with some version other than `latest`:

```sh
docker tag ${image_name}:latest ${image_name}:${image_version}
```

## Creating a Dockerfile

Now we should understand the anatomy of the `Dockerfile` and what each instruction can do for us.

### Specify a base image to use at the start of the Dockerfile

Sometimes I want a variable available at build time but that does not persist in the image. `ARG` is a way of defining a variable that is evaluated at build time. Here I use it to provide a default value for an image repository tag. `FROM` specifies a base image to use. I typically determine an appropriate tag by browsing Docker Hub.

```docker
ARG from_tag=3.7.2-alpine3.8
FROM python:${from_tag}
```

The `ARG` value here can later be overridden from the `build` command:

```sh
docker build --build-arg from_tag=3.7.1-alpine3.8 --rm -t ${image_name} .
```

### Add descriptive labels to the image

Labels are used to capture metadata about the image. The recommended best practice is one label per line, for readability. With Docker at time of writing this only creates one layer.

```docker
LABEL maintainer=mattorama
LABEL description="demonstration container"
```

### Set a working directory

Docker recommends that working directories be set using the `WORKDIR` instruction, rather than sprinkling `cd ..` throughout the `Dockerfile`. Again, this can be set with a default or a build-arg.

```docker
ARG wd=root
WORKDIR ${wd}
```

### Install some OS packages

I prefer to keep these in a separate text file that is copied to the image. Docker recommends that the package manager runs an update once for all installs. As a best practice all packages should be installed at once to avoid conflicting version requirements on dependencies. I invoke `sed` here to manipulate the `\n` characters into a single space to help the package manager.

```docker
COPY os_requirements.txt ./
RUN apk update && \
    apk add --no-cache $(sed -e :a -e '$!N; s/\n/ /; ta' os_requirements.txt)
```

### Install python packages

My use case usually requires some Python packages to be installed. These package requirements are also kepy in a text file.

```docker
COPY py_requirements.txt ./
RUN pip install --no-cache-dir -r py_requirements.txt
```

### Add environment variables

`ENV` is used to set a default environment variable available to the container.

```docker
ENV ev_container=boismint
```

### Setting environment variables during image build

`ARG` is used to set a default for an ENV in the Dockerfile:

```docker
ARG buildtime_variable=moutiere
ENV ev_buildtime=$buildtime_variable
```

The `buildtime_variable` can then be overridden at buildtime:

```sh
docker build --build-arg buildtime_variable=peyron -t ${image_name} .
```

Or by using an environment variable using dollar substitution:

```sh
export ORELLE=rosael
docker build --build-arg buildtime_variable=${ORELLE} -t ${image_name} .
```

To see what the variables are in the image, use `docker inspect ${image_name}`.

### Setting environment variables during container run

To set at runtime, i.e., not in the image but in the container, you can use the `--env` option.

```sh
docker run --rm --env ev_runtime=bouchet -it ${image_name}
```

Although the environment variable does not need to be declared in the `Dockerfile`, if it is declared it must have a default value set.

### Exposing ports and port forwarding

Within the `Dockerfile` ports on the container can be exposed. It is best practice to expose only the ports the service needs, and to use the standard ports on the container, e.g., `5432` for a PostgreSQL database.

```docker
EXPOSE 5432
```

On the host machine, there may already be something using the port exposed by the container. We can then define port forwarding at run time using the `run` command. The first port is the host port, the second port is the exposed container port.

```sh
docker run --rm -p 15432:5432 -it ${image_name}
```

### Volumes on the host accessible by the container

There are a couple of use cases I have had for volumes. One is to persist data after a container stops, such as for a database. Another is to edit files locally and have them available to the container. The `VOLUME` instruction accomplishes this mapping.

First create a directory on the host with something that the container should see.

```sh
mkdir host_dir
echo "Hello, world!" > host_dir/greeting.txt
```

In the `Dockerfile`, declare the location of the directory on the container.

```docker
VOLUME /external_dir
```

At run time, specify the path mapping of the volume from host to container.

```sh
docker run --rm -v $PWD/host_dir/:/external_dir -it ${image_name}
```

### The `CMD` instruction for provide defaults for an executable container

There should only be one `CMD` instruction. It should do the most obvious thing.

```docker
CMD ["bash"]
```

Invoking `docker run` will then execute this command (and its arguments).

```sh
docker run --rm -it ${image_name}
```

To override the `CMD` instruction at runtime, just give another command and its arguments to be executed.

```sh
docker run --rm -it ${image_name} python
```

### The `ENTRYPOINT` instruction for running a container as an executable

In the `Dockerfile`, we can define instructions to execute at runtime, along with arguments that can be overridden at runtime. In the instructions below, the `ENTRYPOINT` instruction runs the `echo` command with one argument, and the `CMD` instruction provides the second argument.

```docker
ENTRYPOINT ["/bin/echo", "Hello"]
CMD ["world"]
```

The argument in `CMD` will be used with those in `ENTRYPOINT`:

```sh
docker run --rm ${image_name}
```

The argument to `CMD` can be overridden at runtime:

```sh
docker run --rm ${image_name} mattorama
```

### Using runtime environment variables with an entrypoint instruction

The `ENTRYPOINT` is pertinent for a container that is a running service. It is best practice to have more involved instructions use a script of the same name. For example:

* Create an `entrypoint.sh` file with:

```sh
#!/usr/bin/env bash

# argument given is keyword to run app or otherwise
case "$1" in
    app)
        exec python app.py
        ;;
    default)
        echo "Hello, world, from bash."
        ;;
    *)
        exec "$@"
        ;;
esac
```

* Create an `app.py` file:

```python
#!/usr/bin/env python3

print('Hello, world, from python.')
```

Along with the `Dockerfile` instructions:

```docker
COPY app.py ./
COPY entrypoint.sh ./
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["default"]
```

Three (of many) possible ways to use `docker run` are now (i) to use the default, (ii) to use the app, (iii) to do something else (that is supported by the container):

```sh
docker run --rm ${image_name}
docker run --rm ${image_name} app
docker run --rm ${image_name} bash -c env|grep ev_
```

Observe that the first argument to the `entrypoint.sh` script is optional, because it is provided with a default in the `CMD` instruction.

## Other things I have found useful

### Bulk removal of images

I created a lot of images without a name and I wanted to clean them up. There is no built in docker command to remove these images. Here is a bonus command I created to remove all images with the name `<none>`. It parses the output from `docker image ls`, extracts image ids, transforms to space separated, then runs `docker rmi` with the image ids as arguments.

```sh
docker rmi -f $(docker image ls | grep '<none>' | grep -Eo [0-9a-z]{12} | sed -e :a -e '$!N; s/\n/ /; ta')
```

### Bulk removal of containers

I created a lot of containers. I want to remove all of the ones that have, say, `Exited`.

```sh
docker rm $(docker ps -a | grep Exited | awk '{print $1}')
```

### ARG vs ENV

`ARG` is available to the Dockerfile and while the image is built. `ARG` is not available to the image or the container. `ENV` is available while the image is built, and in the image and the container. `ENV` is not available in the Dockerfile. `ARG` values can be used to set defaults for `ENV` values. There is a nice writeup [here](https://vsupalov.com/docker-build-pass-environment-variables/)

### COPY vs ADD

Both commands add things to the image. `COPY` is limited to moving files from host to container, and is recommended for most cases by Docker. `ADD` supports other sources such as URLs and tarballs. `ADD` thus may increase image size so it is preferred to use `RUN curl...` instead.

### CMD vs RUN

`RUN` is a build instruction, used when creating the image, of which there may be many such instructions. `CMD` is a run instruction, defining what should be done when a container is launched from the image, and there can only be one such instruction. `CMD` is the default instruction for the container.

### CMD vs ENTRYPOINT

A `Dockerfile` must have at least one of `CMD` and `ENTRYPOINT`. These instructions are used to capture things that must occur at runtime, but which are not necessarily known at buildtime, for example host configuration and environemnt variables. `CMD` can be used in tandem with `ENTRYPOINT` to change the parameters most likely to need tweaking. The diagram [here](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact) gave me clarity.

### `docker run` vs `docker exec`

For my purposes, `run` is used for launching a container from an image, and `exec` is used for running a command on a running container. For adhoc commands during development, `run` can also be used, as I have shown above:

```sh
docker run --rm  -i -t ${image_name}
```

To leave a container running, use the `-d` flag for detached mode. I like to capture the container id as a variable to then use with `exec` and `stop`.

```sh
cid=$(docker run --rm -d -i -t ${image_name} bash)
docker exec -it ${cid} bash
docker stop ${cid}
```

## Summary

I have introduced Docker and the `build` and `run` commands for creating individual containers. I have demonstrated how to interact with the containers and configure environment variables at run time. I have presented the differences between some Docker instructions that are often confused or misunderstood.
