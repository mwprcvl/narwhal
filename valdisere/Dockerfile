# Use miniconda3 base image
ARG base_tag=4.5.12
FROM continuumio/miniconda3:${base_tag}

# Copy the environment file so conda environment can be created
#COPY environment.yml .
COPY ./py_notebooks/explicit.yml environment.yml
RUN /opt/conda/bin/conda env create --file environment.yml && \
  /opt/conda/bin/conda clean -tipsy

# Add the CONDA_USER to avoid running container as root
ARG conda_user=appuser
ARG conda_home=/app

# Explicitly set user/group IDs for a non-root user
# also create the user's home directory with appropriate permissions
RUN set -eux; \
  groupadd -r ${conda_user} --gid=999; \
  useradd -r -g ${conda_user} --uid=999 --home-dir=${conda_home} \
    --shell=/bin/bash ${conda_user}; \
  mkdir -p ${conda_home}; \
  chown -R ${conda_user}:${conda_user} ${conda_home}

# activate the environment for the user
ENV USER=${conda_user}
USER ${USER}
WORKDIR ${conda_home}
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate valdisere" >> ~/.bashrc

# port for jupyter
EXPOSE 8888

# Run bash upon entry to keep alive
CMD [ "/bin/bash" ]
