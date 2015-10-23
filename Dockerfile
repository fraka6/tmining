FROM ubuntu:trusty
MAINTAINER Kamil Trzciński <ayufan@ayufan.eu>

RUN apt-get -y install python-pip python-dev g++ make libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev gfortran

