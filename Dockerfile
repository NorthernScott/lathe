# Build from debian bookworm image
FROM debian:bookworm

# Set environment variables and arguments
ENV APP_NAME=lathe
ENV APP_USER=dev
ENV APP_USER_PASSWORD=dev
ENV APP_USER_HOME="/home/${APP_USER}"
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.12

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
WORKDIR ${APP_USER_HOME}
COPY --chown=${APP_USER}:${APP_USER} [".home/", "${APP_USER_HOME}"]
RUN source ${APP_USER_HOME}/.bashrc
ENV PYENV_ROOT="${APP_USER_HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${APP_USER_HOME}/.local/bin:$PATH"

# Install pyenv, Python, and Poetry

# RUN ["curl", "https://pyenv.run"]
# RUN ["pyenv", "install", "${PYTHON_VERSION}"]
# RUN ["pyenv", "global", "${PYTHON_VERSION}"]
# RUN ["curl", "-sSL", " https://install.python-poetry.org", "|", "python3", "-"]
# RUN ["poetry", "config", "virtualenvs.in-project true"]
# RUN ["poetry", "completions", "bash >> ${APP_USER_HOME}/.bash_completion"]

RUN DEBIAN_FRONTEND=noninteractive \
    && echo "Fetching PyEnv" \
    && curl https://pyenv.run | bash \
    && echo "Installing Python" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "Installing Global Python" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "Installing & Configuring Poetry" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true \
    && poetry completions bash >> ${APP_USER_HOME}/.bash_completion

# Add project files
COPY --chown=${APP_USER}:${APP_USER} ["src/", "/opt/${APP_NAME}"]

# Create health check
COPY ["./appHealthCheck.sh", "/bin/appHealthCheck.sh"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD ["bash", "/bin/appHealthCheck.sh"]

# Start and update shell
ENTRYPOINT ["/bin/bash"]