# Use miniconda3 base image
ARG base_tag="4.5.12"
FROM continuumio/miniconda3:${base_tag}

# Copy the environment file so conda environment can be created
ARG environment_file="environment.yml"
COPY ${environment_file} environment.yml
RUN /opt/conda/bin/conda env create --file environment.yml && \
    /opt/conda/bin/conda clean -tipsy

# Add the appuser to avoid running container as root
ARG srcdir="app"
ARG user="appuser"
ARG home=/usr/local/${user}


# Explicitly set user/group IDs for a non-root user
# also create the user's home directory with appropriate permissions
RUN set -eux; \
    groupadd -r ${user} --gid=999; \
    useradd -r -g ${user} --uid=999 --home-dir=${home} \
    --shell=/bin/bash ${user}; \
    mkdir -p ${home}; \
    chown -R ${user}:${user} ${home}

# activate the environment for the user
ENV USER=${user}
USER ${user}
WORKDIR ${home}
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate appenv" >> ~/.bashrc

# port for jupyter
EXPOSE 8888

WORKDIR /

# Run bash upon entry to keep alive
CMD [ "/bin/bash" ]
