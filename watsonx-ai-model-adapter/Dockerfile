FROM mambaorg/micromamba:latest

WORKDIR /code

COPY ./environment.yml /code/environment.yml

RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

COPY ./main.py /code/main.py

#Support arbitrary user ids: https://docs.openshift.com/container-platform/4.8/openshift_images/create-images.html#images-create-guide-openshift_create-images
USER root

RUN chgrp -R 0 /opt  && chmod -R g=u /opt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
