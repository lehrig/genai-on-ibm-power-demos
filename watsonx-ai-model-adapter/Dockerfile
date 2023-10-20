FROM quay.io/ibm/kubeflow-notebook-image-ppc64le@sha256:fa6b3a065b14a206895531f99e8aafa1fcaba3def4d000f13dbe9e495c1aad32

RUN mamba install \
        --yes \
        'conda-forge::uvicorn'

COPY start.sh /usr/local/bin/
COPY --chown="${NB_UID}:${NB_GID}" main.py "${HOME}"

USER root
RUN fix-permissions /usr/local/bin/ && \
    chmod +x /usr/local/bin/start.sh

USER ${NB_UID}
EXPOSE 8080
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start.sh"]
