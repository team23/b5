#!/usr/bin/env bash

NPM_PATH="."

npm:run() {
    (
        cd "${NPM_PATH}" && \
        npm "$@"
    )
}

npm:install() {
    npm:run install
}

npm:update() {
    npm:run update
}

npm:runbin() {
    (
        if [ -d "${NPM_PATH}/node_modules" ]
        then
            PATH="${NPM_PATH}/node_modules/.bin:${PATH}"
        fi
        "$@"
    )
}

task:npm() {
    npm:run "$@"
}
