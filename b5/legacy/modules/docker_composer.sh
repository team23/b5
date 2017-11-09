#!/usr/bin/env bash

b5:module_load docker

DOCKER_COMPOSER_SERVICE="php"
DOCKER_COMPOSER_USER="www-data"
DOCKER_COMPOSER_PATH="/app/build"
DOCKER_COMPOSER_VENDOR_DIR="/app/vendor"
DOCKER_COMPOSER_RUNBIN_SCRIPT="/opt/composer_runbin.sh"

docker_composer:docker_container_run() {
    docker:container_run \
                        -e DOCKER_COMPOSER_PATH="${DOCKER_COMPOSER_PATH}" \
                        -e DOCKER_COMPOSER_VENDOR_DIR="${DOCKER_COMPOSER_VENDOR_DIR}" \
                        -w "${DOCKER_COMPOSER_PATH}" \
                        "${DOCKER_COMPOSER_SERVICE}" "$@"
}

docker_composer:run() {
    docker_composer:docker_container_run composer "$@"
}

docker_composer:install() {
    docker_composer:run install
}

docker_composer:update() {
    docker_composer:run update
}

docker_composer:runbin() {
    docker_composer:docker_container_run "${DOCKER_COMPOSER_RUNBIN_SCRIPT}" "$@"
}

task:composer() {
    docker_composer:run "$@"
}
