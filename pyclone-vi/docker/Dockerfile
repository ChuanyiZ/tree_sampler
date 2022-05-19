FROM continuumio/miniconda3:latest

WORKDIR /home
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge

# Install pyclone-vi

RUN wget https://raw.githubusercontent.com/Roth-Lab/pyclone-vi/master/requirements.txt
RUN conda create -n pyclone-vi --file requirements.txt --yes
RUN conda run -v -n pyclone-vi pip install -v git+https://github.com/Roth-Lab/pyclone-vi.git

# Reduce the size of the image
RUN conda clean --all --yes

# Let RUN command use pyclone-vi env
SHELL ["conda", "run", "-n", "pyclone-vi", "/bin/bash", "-c"]

# # Test
# RUN pyclone-vi --help

# # copy the phyloflow/pyclone/code directory into the container. 
# # NOTE this says the local code is in '.' b/c the build_pyclone_container.sh script 
# # uses  '..' as the context for the build process. Necessary to avoid this issue:
# # https://stackoverflow.com/questions/27068596/how-to-include-files-outside-of-dockers-build-context
# COPY ./code /code
