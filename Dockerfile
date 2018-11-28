# currently using this image as it supports Rpi0
FROM resin/rpi-raspbian:stretch
#FROM resin/raspberry-pi-python:3.7-stretch # testing to find a python3 imagage that supports arm6

LABEL Name=docker-pi-zero-phat Version=0.0.1

# enable container init system.
ENV INITSYSTEM on

# add the missing packages, it would be greate to switch to a python3 image where some of this can be skipped
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    libffi-dev \
    i2c-tools \
    python3-smbus \
    python3-rpi.gpio \
    python3-envirophat \
    python3-automationhat \
    && pip3 install paho-mqtt --no-cache-dir \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# add the python service and (future) config file
ADD mqtt-worker.py config.yml /

# command to start the python3 service
CMD ["python3", "./mqtt-worker.py"]