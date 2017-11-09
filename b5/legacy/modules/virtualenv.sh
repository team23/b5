#!/usr/bin/env bash

VIRTUALENV_PATH="../ENV"
VIRTUALENV_PYTHON_EXE="python"
VIRTUALENV_REQUIREMENTS_FILE="requirements.txt"

virtualenv:run() {
    (
        # if [ -d "${VIRTUALENV_PATH}" ]
        # then
        #     PATH="${VIRTUALENV_PATH}/bin:${PATH}"
        # fi
        source "${VIRTUALENV_PATH}/bin/activate" && \
        "$@"
    )
}

virtualenv:update() {
    virtualenv:run pip install -U -r "${VIRTUALENV_REQUIREMENTS_FILE}"
}

virtualenv:install() {
    virtualenv --python="${VIRTUALENV_PYTHON_EXE}" "${VIRTUALENV_PATH}" && \
    virtualenv:update
}

task:pip() {
    virtualenv:run pip "$@"
}
