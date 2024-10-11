# Build from debian bookworm image
FROM debian:bookworm-slim AS baseimage
SHELL ["/bin/bash", "-c"]

# Set environment variables and arguments
ARG APP_NAME="lathe"
ARG APP_USER="dev"
ARG APP_USER_HOME="/home/${APP_USER}"
ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.12

ENV PYENV_ROOT="${APP_USER_HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${APP_USER_HOME}/.local/bin:$PATH"

# Create health check
COPY ["./appHealthCheck.sh", "/bin/appHealthCheck.sh"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD ["bash", "/bin/appHealthCheck.sh"]

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

# Create user
RUN --mount=type=secret,id=app_user_password \
    export APP_USER_PASSWORD=$(cat /run/secrets/app_user_password) \
    && echo ${APP_USER_PASSWORD} \
    && useradd -md ${APP_USER_HOME} -s /bin/bash -p ${APP_USER_PASSWORD} -g root -G sudo ${APP_USER} \
    && echo "${APP_USER}:${APP_USER_PASSWORD}" | chpasswd

# Copy source files
COPY --chown=${APP_USER}:root ["src/", "/opt/${APP_NAME}"]

# Install pyenv, Python, and Poetry
USER ${APP_USER}
RUN DEBIAN_FRONTEND=noninteractive \
    && echo "Installing PyEnv" \
    && curl https://pyenv.run | bash \
    && echo "Installing Python" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "Installing Global Python" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "Installing & Configuring Poetry" \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true \
    && poetry completions bash >> ${APP_USER_HOME}/.bash_completion 

# Start shell
ENTRYPOINT ["/bin/bash"]