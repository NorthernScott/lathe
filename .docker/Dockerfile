# Build from debian bookworm image
FROM python:3.13-slim-bullseye AS baseimage
SHELL ["/bin/bash", "-c"]

# Set environment variables and arguments
ARG APP_NAME="lathe"
ARG APP_USER="dev"
ARG APP_USER_HOME="/home/${APP_USER}"
ARG APP_SRC="/${APP_USER}/src/${APP_NAME}"

# Create health check
COPY [".docker/appHealthCheck.sh", "/bin/appHealthCheck.sh"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --start-interval=5s --retries=3 CMD ["bash", "/bin/appHealthCheck.sh"]

# Install system packages
RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends

# Create user
RUN --mount=type=secret,id=app_user_password \
    export APP_USER_PASSWORD=$(cat /run/secrets/app_user_password) \
    && echo ${APP_USER_PASSWORD} \
    && useradd -md ${APP_USER_HOME} -s /bin/bash -p ${APP_USER_PASSWORD} -g root -G sudo ${APP_USER} \
    && echo "${APP_USER}:${APP_USER_PASSWORD}" | chpasswd

# Copy source files
COPY --chown=${APP_USER}:root ["src/", "${APP_SRC}"]

# Install pyenv, Python, and Poetry
USER ${APP_USER}
WORKDIR ${APP_SRC}


# Install dependencies
RUN poetry install -C /opt/${APP_NAME}

# Start shell
WORKDIR /opt/${APP_NAME}
ENTRYPOINT ["/bin/bash"]