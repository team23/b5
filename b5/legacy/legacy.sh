#!/usr/bin/env bash

b5:warn_legacy() {
    b5:warn "DEPRECATION: You used a legacy function, better stop that (${1:-})"
}

b5:warn_legacy "legacy module itself, see config.yml"

# b5 install module part

b5:install() {
    b5:warn_legacy "b5:install"
    if [ -e "local.example.yml" ] && [ ! -e "local.yml" ]
    then
        cp "local.example.yml" "local.yml"
        echo
        echo -e "${B5_FONT_GREEN}IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT${B5_FONT_RESTORE}"
        echo
        echo "Copied local.example.yml to local.yml"
        echo "Make sure to edit local.yml now"
        echo
        echo -e "${B5_FONT_GREEN}IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT${B5_FONT_RESTORE}"
        echo
    fi
}

# Module handling

declare -a LEGACY_MODULES_LOADED
LEGACY_MODULES_LOADED+=("b5")
LEGACY_MODULES_LOADED+=("Taskfile")
LEGACY_MODULES_LOADED+=("Taskfile.local")

b5:module_exists() {
    b5:warn_legacy "b5:module_exists"
    if [ -z "${1:-}" ]
    then
        echo "Usage: b5:module_exists <module_name>"
        return 254
    fi
    if [ -e "${LEGACY_MODULES_PATH}/${1}.sh" ]
    then
        return 0
    else
        echo "${LEGACY_MODULES_PATH}"
        return 1
    fi
}

b5:module_load() {
    b5:warn_legacy "b5:module_load"
    if [ -z "${1:-}" ]
    then
        echo "Usage: b5:module_load <module_name>"
        return 254
    fi
    if [[ " ${LEGACY_MODULES_LOADED[*]} " == *" $1 "* ]]
    then
        return 0
    fi
    if ( b5:module_exists "$1" )
    then
        source "${LEGACY_MODULES_PATH}/${1}.sh" && \
        LEGACY_MODULES_LOADED+=("$1")
    else
        echo -e "${B5_FONT_RED}Module $1 not found${B5_FONT_RESTORE}"
        echo -e "${B5_FONT_RED}ABORTING!${B5_FONT_RESTORE}"
        exit 250
    fi
}

b5:module_has() {
    b5:warn_legacy "b5:module_has"
    local module="${1:-}"
    local action="${2:-}"
    if [ -z "$action" ] || [ -z "$module" ]
    then
        echo "Usage: b5:module_run <module> <module_action>"
        return 254
    fi

    local type_result=$( type -t "${module}:${action}" )
    if [ "$type_result" == "function" ]
    then
        return 0
    else
        return 1
    fi
}

b5:module_run() {
    b5:warn_legacy "b5:module_run"
    local module="${1:-}"
    local action="${2:-}"
    if [ -z "$action" ] || [ -z "$module" ]
    then
        echo "Usage: b5:module_run <module> <module_action>"
        return 254
    fi
    shift 2

    echo "Calling ${module}:${action}" && \
        "${module}:${action}" "$@" && \
        echo
}

b5:module_run_all() {
    b5:warn_legacy "b5:module_run_all"
    local action="${1:-}"
    if [ -z "$action" ]
    then
        echo "Usage: b5:module_run_all <module_action>"
        return 254
    fi
    shift

    for module in ${LEGACY_MODULES_LOADED[@]}
    do
        if b5:module_has "${module}" "${action}"
        then
            b5:module_run "${module}" "${action}" "$@"
        fi
    done
}

# Legacy tasks

if [ ! -z "${PROJECT_PATH}" ]
then
    task:install() {
        b5:module_run_all install
    }

    task:update() {
        b5:module_run_all update
    }

    task:clean() {
        b5:module_run_all clean
    }
fi
