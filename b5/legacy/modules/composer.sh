#!/usr/bin/env bash

COMPOSER_PATH="."
COMPOSER_VENDOR_DIR="../vendor"

composer:run() {
    (
        cd "${COMPOSER_PATH}" && \
        composer "$@"
    )
}

composer:install() {
    composer:run install
}

composer:update() {
    composer:run update
}

composer:runbin() {
    (
        if [ -d "${COMPOSER_VENDOR_DIR}/bin" ]
        then
            PATH="${COMPOSER_VENDOR_DIR}/bin/:${PATH}"
        fi
        "$@"
    )
}

task:composer() {
    composer:run "$@"
}
