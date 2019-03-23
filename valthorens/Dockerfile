# use a base image with small OS and small Python installed
ARG from_tag=3.7.2-alpine3.8
FROM python:${from_tag}

# add descriptive labels
LABEL maintainer=mattorama
LABEL description="demonstration container"
LABEL url="link_to_repo"

# best practice to set a working directory from an environment variable
ARG wd=root
WORKDIR ${wd}

# used to install OS packages
COPY os_requirements.txt ./
RUN apk update && \
    apk add --no-cache $(sed -e :a -e '$!N; s/\n/ /; ta' os_requirements.txt)
# sed from here: https://unix.stackexchange.com/questions/108782/pass-the-output-of-previous-command-to-next-as-an-argument

# used to install python packages
COPY py_requirements.txt ./
RUN pip install --no-cache-dir -r py_requirements.txt

# set an environment variable available in the container
ENV ev_container=boismint

# create an environment variable at build time
ARG buildtime_variable=moutiere
ENV ev_buildtime=$buildtime_variable

# create an environment variable at run time with default at buildtime
ENV ev_runtime=tyrolienne

# expose ports
EXPOSE 5432

# mount host volume
VOLUME ["/external_dir"]

# an example CMD for use without an ENTRYPOINT
#CMD ["bash"]

# an example for ENTRYPOINT with CMD
#ENTRYPOINT ["/bin/echo", "Hello"]
#CMD ["world"]

# an example entrypoint script with default arguments from CMD
COPY app.py ./
COPY entrypoint.sh ./
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["default"]
