ARG base_tag="3.7.4-stretch"
FROM python:${base_tag}

# copy the requirements file so environment can be created
ARG requirements_file="requirements.txt"
COPY ${requirements_file} requirements.txt
# install python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# port for vscode
EXPOSE 3000

# port for flask
EXPOSE 5000

# port for dash
EXPOSE 8050

# port for airflow
EXPOSE 8080

# Run bash upon entry to keep alive
CMD [ "/bin/bash" ]

# set up directories
ARG airflow_home=/airflow
ARG dags_home=/airflow/dags
ARG data_volume=/data
ARG python_path=/app
RUN mkdir -p ${airflow_home}/dags && \
    mkdir ${data_volume} && \
    mkdir ${python_path}
