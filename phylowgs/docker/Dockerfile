# This container installs phylowgs
FROM gcc:9.2 AS build

WORKDIR /home
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN wget ftp://ftp.gnu.org/gnu/gsl/gsl-2.7.tar.gz && \
    tar -zxvf gsl-2.7.tar.gz && \
    cd gsl-2.7 && \
    mkdir /home/gsl && \
    ./configure --prefix=/home/gsl && \
    make && \
    make check && \
    make install

RUN ls -al /home/gsl && \
    ls -al /home/gsl/bin && \
    ls -al /home/gsl/include

# ENV C_INCLUDE_PATH="/home/gsl/include:$C_INCLUDE_PATH"
ENV CPLUS_INCLUDE_PATH="/home/gsl/include:$CPLUS_INCLUDE_PATH"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/gsl/lib"

RUN git clone https://github.com/morrislab/phylowgs.git && \
    cd phylowgs && \
    git checkout 681df79 && \
    g++ -o mh.o -O3 -I/home/gsl/include -L/home/gsl/lib -lgsl -lgslcblas -lm mh.cpp  util.cpp

# `/home/gsl/bin/gsl-config --cflags --libs`

###############
# Finish build
###############

FROM python:2.7

WORKDIR /home
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/gsl/lib"

COPY --from=build /home/gsl /home/gsl

COPY --from=build /home/phylowgs /home/phylowgs

COPY ./code /code

RUN pip install numpy scipy ete2 pyvcf pandas

RUN cp /code/*.py /home/phylowgs/parser && \
    cd /home/phylowgs && \
    git apply /code/all.patch

# test
# RUN cd /home/phylowgs && \
#     python multievolve.py --num-chains 4 --ssms ssm_data.txt --cnvs cnv_data.txt --burnin-samples 1 --mcmc-samples 1
