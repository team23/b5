#!/usr/bin/env bash

b5:module_load docker

DOCKER_DJANGO_PATH="."
DOCKER_DJANGO_SERVICE="web"
DOCKER_DJANGO_MANAGE_PATH="${DOCKER_DJANGO_PATH}/manage.py"

docker_django:run() {
    docker:container_run "${DOCKER_DJANGO_SERVICE}" python "${DOCKER_DJANGO_MANAGE_PATH}" "$@"
}

docker_django:update() {
    docker_django:run migrate
}

task:django() {
    docker_django:run "$@"
}
