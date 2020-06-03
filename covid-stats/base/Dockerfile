FROM jupyter/scipy-notebook:7d427e7a4dde

# How to run: docker run -v /Users/santteegt/decentraminds/c2d\ demos/mount:/data -it santteegt/stats-demo:latest

USER root

RUN mkdir -p /data/inputs && \
    mkdir -p /data/outputs

RUN fix-permissions /data

WORKDIR /data

RUN conda install -c conda-forge nbpresent altair --yes && \
    pip install wget && \
    conda clean --all -f -y

ENTRYPOINT ["python", "/data/script.py"]

USER $NB_UID