#!/usr/bin/env bash

DRUPAL_PATH="../web"
DRUPAL_PHP_BIN="php"
DRUPAL_DRUSH_PATH="../_drush"
DRUPAL_DRUSH_BIN="${DRUPAL_DRUSH_PATH}/drush.php"
DRUPAL_DRUSH_BRANCH='6.x'

drupal:install() {
    if [ ! -d "${DRUPAL_DRUSH_PATH}" ]
    then
        mkdir -p "${DRUPAL_DRUSH_PATH}" && \
        git clone --depth 1 --branch "${DRUPAL_DRUSH_BRANCH}" https://github.com/drush-ops/drush.git "${DRUPAL_DRUSH_PATH}"
    fi
}

drupal:run() {
    (
        "${DRUPAL_PHP_BIN}" "${DRUPAL_DRUSH_BIN}" --php="${DRUPAL_PHP_BIN}" "$@"
    )
}

task:drush() {
    drupal:run "$@"
}
