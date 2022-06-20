FROM gcc:9.2 AS build

WORKDIR /home
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN git clone https://github.com/morrislab/pairtree.git && \
    cd pairtree/lib && \
    git checkout 2fd9f95 && \
    git clone https://github.com/jwintersinger/projectppm && \
    cd projectppm && \
    git checkout 9b0289f && \
    bash make.sh

###############
# Finish build
###############

FROM python:3.7
# FROM continuumio/miniconda3:latest

WORKDIR /home
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY --from=build /home/pairtree /home/pairtree

# RUN conda create --name pairtree -c conda-forge python=3.7 numpy scipy scikit-learn tqdm numba colorlover plotly
# SHELL ["conda", "run", "-n", "pairtree", "/bin/bash", "-c"]

RUN pip install numpy scipy scikit-learn tqdm numba colorlover plotly pickle pandas 

COPY ./code/getParams.py ./code/printtree.py .code/clusterToMutationMapping.py ./code/collectTrajectories.py /home/pairtree/misc/

RUN mkdir -p /home/patch

COPY ./code/*.patch /home/patch

RUN cd /home/pairtree/ && \
    git apply /home/patch/all.patch


# ######## Test
RUN cd /home/pairtree/example && \
    mkdir results && \
    cd results && \
    python /home/pairtree/bin/pairtree --params /home/pairtree/example/example.params.json /home/pairtree/example/example.ssm example.results.npz && \
    python /home/pairtree/bin/plottree --runid example /home/pairtree/example/example.ssm /home/pairtree/example/example.params.json example.results.npz example.results.html
