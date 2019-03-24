# Use rocker/verse base image
ARG base_tag="3.5.2"
FROM rocker/verse:${base_tag}

# add packages
RUN Rscript -e 'devtools::install_version("plotly", version = "4.8.0", repos = "http://cran.us.r-project.org")' && \
  Rscript -e 'devtools::install_version("caret", version = "6.0-81", upgrade = "never", repos = "http://cran.us.r-project.org")' && \
  Rscript -e 'devtools::install_version("xgboost", version = "0.81.0.1", upgrade = "never", repos = "http://cran.us.r-project.org")' && \
  Rscript -e 'devtools::install_version("MatchIt", version = "3.0.2", upgrade = "never", repos = "http://cran.us.r-project.org")'

# launch rstudio in browser as default
WORKDIR /home/rstudio
