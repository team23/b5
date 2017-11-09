#!/usr/bin/env bash

DJANGO_PATH="../web"
DJANGO_MANAGE_PATH="${DJANGO_PATH}/manage.py"

b5:module_load virtualenv

django:run() {
    (
        virtualenv:run python "$DJANGO_MANAGE_PATH" "$@"
    )
}

django:update() {
    django:run migrate
}

task:django() {
    django:run "$@"
}
