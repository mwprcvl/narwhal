ARG base_tag="1386e2046833"
FROM jupyter/minimal-notebook:${base_tag}

USER $NB_UID

# Install Python 3 packages
RUN conda install --quiet --yes \
    'conda-forge::blas=*=openblas' \
    'matplotlib=3.1.*' \
    'pandas=0.25*' \
    'scikit-learn=0.21*' \
    'scipy=1.3*' \
    'statsmodels=0.10*' \
    'conda-forge::airflow=1.10*' \
    'conda-forge::dash=1.4*' \
    'conda-forge::dash-daq=0.2*' \
    'conda-forge::ipdb=0.12*' \
    'conda-forge::psycopg2=2.8*' \
    'conda-forge::pylint=2.4*' \
    'conda-forge::pytest=5.2*' \
    && \
    conda clean --all -f -y && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions /home/$NB_USER

# port for vscode
EXPOSE 3000

# port for flask
EXPOSE 5000

# port for dash
EXPOSE 8050

# port for airflow
EXPOSE 8080

# port for jupyter
EXPOSE 8888

ARG airflow_home=/home/$NB_USER/airflow
ARG data_volume=/home/$NB_USER/data
ARG jupyter_home=/home/$NB_USER/lab
ARG python_path=/home/$NB_USER/app
RUN mkdir -p ${airflow_home}/dags && \
    mkdir ${data_volume} && \
    mkdir ${python_path} && \
    mkdir ${jupyter_home} && \
    fix-permissions /home/$NB_USER

USER $NB_UID

# Run bash upon entry to keep alive
CMD [ "/bin/bash" ]
