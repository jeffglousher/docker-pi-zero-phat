# currently using this image as it supports Rpi0, will later test resin/raspberry-pi-python OR another option to keep python3 support with a small image on RPi0
FROM resin/rpi-raspbian:stretch

LABEL Name=docker-pi-zero-phat Version=0.0.1

ADD mqtt-worker.py /

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
#    python3-dev \
    python3-pip \
#    python3-virtualenv \
    libffi-dev \
    i2c-tools \
#    libraspberrypi-bin \
    python3-smbus \
    python3-rpi.gpio \
    python3-envirophat \
    python3-automationhat \
#    && rm -rf /var/lib/apt/lists/* \
    && pip3 install paho-mqtt --no-cache-dir \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*
    #&& apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && rm -rf /var/lib/apt/lists/*

CMD ["python3", "./mqtt-worker.py"]