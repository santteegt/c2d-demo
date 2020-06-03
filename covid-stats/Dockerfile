FROM santteegt/stats-demo:latest

USER root

# For local development only
# RUN mkdir -p /data/inputs && \
#     mkdir -p /data/outputs
# RUN fix-permissions /data/inputs && \
#     fix-permissions /data/outputs
# COPY data/* /data/inputs/ 

WORKDIR /notebook

COPY notebook_stats.ipynb .

# COPY script.py .

# RUN conda install -c conda-forge nbpresent altair --yes && \
# #     conda install -c damianavila82 rise--yes && \
#     pip install wget && \
#     conda clean --all -f -y

ENTRYPOINT ["python", "/data/script.py"]

USER $NB_UID