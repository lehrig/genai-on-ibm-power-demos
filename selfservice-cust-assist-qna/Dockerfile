FROM node:20.8-bullseye
LABEL maintainer="Sebastian Lehrig <sebastian.lehrig1@ibm.com>"

ENV CHROME_BIN=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV CONDA_DIR=/opt/conda
ENV SHELL=/bin/bash
ENV NB_USER="jovyan"
ENV NB_UID="1001"
ENV NB_GID="100"

ENV PATH="${CONDA_DIR}/bin:${PATH}"
ENV HOME="/home/${NB_USER}"

ENV DEBUG_MODE="True"
ENV SERVICE_PORT=8050
ENV DASH_URL_BASE_PATHNAME="/selfservice-cust-assist-qn/"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions

RUN chmod a+rx /usr/local/bin/fix-permissions && \
    apt update -qq && apt install -qq -y chromium gnulib tar vim && \
    # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
    echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc && \
    # Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
    # and make sure these dirs are writable by the `users` group.
    groupadd -f --gid 1337 $NB_USER && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    # Cleanup
    fix-permissions "${HOME}" && \
    fix-permissions "${CONDA_DIR}"

USER ${NB_UID}

COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"

WORKDIR /tmp

RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}" && \
    set -x && \
    # mamba setup
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-ppc64le/latest | tar -xvj --strip-components=1 bin/micromamba && \
    # pip setup
    mkdir ~/.pip && \
    echo "[global]" >> ~/.pip/pip.conf && \
    echo "extra-index-url = https://repo.fury.io/mgiessing" >> ~/.pip/pip.conf && \
    # Do as much as possible with conda...
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        # temporary fix for https://github.com/mamba-org/mamba/issues/2882#issuecomment-1746314832
        'conda<23.9.0' \
        # - dash 2.7.0 from conda main channel is old
        # - dash latest is 2.14.0 (see https://github.com/plotly/dash)
        # - "allow_duplicate" in Output was introduced in https://github.com/plotly/dash/pull/2414 with dash 2.9.0 
        # -> getting latest dash from conda-forge
        'conda-forge::dash' \
        'mamba' \
        'pandas==2.0.3' \
        'python-dotenv' \
        'requests' \
    && \
    rm ./micromamba && \
    # Install remainder via pip...
    git clone https://github.com/IBM/dsce-sample-apps.git ${HOME}/dsce-sample-apps && \
    cd "${HOME}"/dsce-sample-apps/selfservice-cust-assist-qna && \
    pip3 install -r requirements.txt && \
    # Continue with Base...
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    # Power customization
    sed -i 's/\/assets\//assets\//g' template.py && \
    sed -i 's/authenticator.token_manager.get_token()/"5wy6n8IBRn27vLi1wdmsxFm8krXIm_ywVZqV8MYejYAn"/g' template.py && \
    fix-permissions "/home/${NB_USER}"

CMD python3 template.py

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"/dsce-sample-apps/selfservice-cust-assist-qna
