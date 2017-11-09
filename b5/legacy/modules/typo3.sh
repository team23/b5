#!/usr/bin/env bash

TYPO3_PATH="../web"

b5:module_load composer

task:typo3() {
    (
        composer:runbin typo3 "$@"
    )
}

task:typo3cms() {
    (
        composer:runbin typo3cms "$@"
    )
}
