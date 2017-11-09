#!/usr/bin/env bash

DOCKER_PATH="."
DOCKER_DATA_PATH="${CONFIG_paths_docker_data:-}"
DOCKER_PROJECT_NAME="${CONFIG_project_key:-$( basename $( dirname `pwd` ) )}"

docker:install() {
    docker:run build
}

docker:update() {
    docker:install
}

docker:run() {
    (
        cd "${DOCKER_PATH}" && \
        COMPOSE_PROJECT_NAME="${DOCKER_PROJECT_NAME}" docker-compose "$@"
    )
}

docker:container_run() {
    if [ ! -z "${DOCKER_RUN_NOTTY:-}" ]
    then
        docker:run run -T --rm "$@"
    else
        docker:run run --rm "$@"
    fi
}

task:docker-compose() {
    docker:run "$@"
}
