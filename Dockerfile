# Build from debian bookworm image
FROM debian:bookworm-slim

# Set environment variables and arguments
ARG APP_NAME=${APP_NAME}
ARG APP_USER=${APP_USER}
ARG APP_USER_HOME="/home/${APP_USER}"
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.12

ENV PYENV_ROOT="${APP_USER_HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${APP_USER_HOME}/.local/bin:$PATH"

# Load user password
RUN --mount=type=secret, id=app_user_password, env=APP_USER_PASSWORD, required=true \
    && echo "App User Password: ${APP_USER_PASSWORD}"
ARG APP_USER_PASSWORD=${APP_USER_PASSWORD}

# RUN echo "App Name: "${APP_NAME}\
#     && echo "App User: "${APP_USER}\
#     && echo "App User Password: "${APP_USER_PASSWORD}\
#     && echo "App User Home: "${APP_USER_HOME}\
#     && echo "Debian Frontend: " ${DEBIAN_FRONTEND}\
#     && echo "Python Version: "${PYTHON_VERSION}\
#     && echo "PyEnv Root: "${PYENV_ROOT}\
#     && echo "Path: "${PATH}

# Create health check
COPY ["./appHealthCheck.sh", "/bin/appHealthCheck.sh"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD ["bash", "/bin/appHealthCheck.sh"]

# Create user
RUN useradd -md ${APP_USER_HOME} -s /bin/bash -p ${APP_USER_PASSWORD} -g root -G sudo ${APP_USER}

# Create project directory
RUN mkdir -p /opt/${APP_NAME}

# Install system packages
RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends make \
    ca-certificates \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    nano \
    sudo 

# Configure shell
SHELL ["/bin/bash", "-c"]
USER ${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} [".home/", "${APP_USER_HOME}"]
RUN source ${APP_USER_HOME}/.bashrc

# Install pyenv, Python, and Poetry
USER root
RUN DEBIAN_FRONTEND=noninteractive \
    && echo "Fetching PyEnv" \
    && curl https://pyenv.run | bash \
    && echo "Installing Python" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "Installing Global Python" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "Installing & Configuring Poetry" \
    && curl -sSL https://install.python-poetry.org | python3 -

RUN DEBIAN_FRONTEND=noninteractive \
    && /root/.local/bin/poetry config virtualenvs.in-project true \
    && /root/.local/bin/poetry completions bash >> ${APP_USER_HOME}/.bash_completion

# Add project files
USER ${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} ["src/", "/opt/${APP_NAME}"]

# Start and update shell
WORKDIR ${APP_USER_HOME}
ENTRYPOINT ["/bin/bash"]