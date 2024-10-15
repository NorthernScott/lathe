# Docker Installation

Start by cloning this repository (https://github.com/NorthernScott/lathe) into an appropriate working directory. Docker build files and compose files, as well as necessary build context files, can be found in the /.docker sub-directory.

## Development Environment

The recommended way to create a dev environment is to use the following cli command from the project root directory: `docker compose -f ".docker/dev-compose.yml" -p lathe up -d --build up` cli command. This will build a Debian-based development environment with the necessary volumes, a bridge network, and links to various containers. **Before building the project, you must create the "app_user_password.txt" file in the /.docker sub-directory. The file should be UTF-8 encoded and contain only the unhashed plain-text password that you would like to use for the dev user. *The build will fail if this file is not present.***

One the project is built, run the cli command `docker attach lathe-app` to attach your terminal to the container. Your default working directory in the container will be /opt/lathe, which is set to sync with the lathe/src directory on your host. You can run the program using `poetry run python3 lathe/lathe.py`. Use the option `--help` to see a list of commands.

## Production Environment

*TBD*