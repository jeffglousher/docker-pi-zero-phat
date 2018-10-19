# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM resin/rpi-raspbian:stretch

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=docker-pi-zero-phat Version=0.0.1
#EXPOSE 3000  

#WORKDIR /app
#ADD . /app
ADD mqtt-worker.py /
# Update APT cache
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

# Clean up APT cache
#RUN rm -rf /var/lib/apt/lists/*

#RUN pip3 install paho-mqtt --no-cache-dir
# Using pip:
#RUN python3 -m pip install -r requirements.txt
CMD ["python3", "./mqtt-worker.py"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "docker-pi-zero-phat"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m docker-pi-zero-phat"
