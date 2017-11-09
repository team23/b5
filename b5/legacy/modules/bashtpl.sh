#!/usr/bin/env bash

BASHTPL_INPUT_1=""
BASHTPL_OUTPUT_1=""
BASHTPL_INPUT_2=""
BASHTPL_OUTPUT_2=""
BASHTPL_INPUT_3=""
BASHTPL_OUTPUT_3=""
BASHTPL_INPUT_4=""
BASHTPL_OUTPUT_4=""
BASHTPL_INPUT_5=""
BASHTPL_OUTPUT_5=""

bashtpl:render() {
    if [ -z "${1:-}" ]
    then
        echo "Usage: bashtpl:render <template_file>"
        return 254
    fi
    if [ ! -e "$1" ]
    then
        echo "Template $1 not found"
        return 253
    fi

    (
        eval "cat <<B5ENDOFINPUT
$( sed -e 's/\$\([^\{\(]\)/\\\$\1/g' "$1" )
B5ENDOFINPUT"
    )
}

bashtpl:build() {
    if [ -z "${1:-}" ] || [ -z "${2:-}" ]
    then
        echo "Usage: bashtpl:build <template_file> <output_file> [force_creation]"
        return 254
    fi

    (
        if [ ! -e "$2" ] || [ ! -z "${3:-}" ]
        then
            bashtpl:render "$1" > "$2"
        fi
    )
}

bashtpl:build_prompt() {
    if [ -z "${1:-}" ] || [ -z "${2:-}" ]
    then
        echo "Usage: bashtpl:build_prompt <template_file> <output_file>"
        return 254
    fi

    local is_newer=0
    local params="yN"
    local response=""
    if [ -e "$2" ]
    then
        echo "File $2 already exists"
        if [ "$1" -nt "$2" ]
        then
            echo "(but template $1 is newer, so probably changed)"
            is_newer=1
            params="Yn"
        fi
        if [ -e "local.yml" ] && [ "local.yml" -nt "$2" ]
        then
            echo "(but local.yml is newer, so probably changed)"
            is_newer=1
            params="Yn"
        fi
        while [ -z "$response" ]
        do
            echo -n "Recreate $2 now? [$params] "
            read response
            case "$response" in
                [yY])
                    bashtpl:build "$1" "$2" force
                    break
                    ;;
                [nN])
                    break
                    ;;
                "")
                    if [ $is_newer -gt 0 ]
                    then
                        bashtpl:build "$1" "$2" force
                    fi
                    break
                    ;;
                *)
                    echo "Invalid input, try again"
                    ;;
            esac
        done
    else
        bashtpl:build "$1" "$2"
    fi
}

bashtpl:install() {
    if [ ! -z "${BASHTPL_INPUT_1}" ] && [ ! -z "${BASHTPL_OUTPUT_1}" ]
    then
        bashtpl:build "${BASHTPL_INPUT_1}" "${BASHTPL_OUTPUT_1}"
    fi
    if [ ! -z "${BASHTPL_INPUT_2}" ] && [ ! -z "${BASHTPL_OUTPUT_2}" ]
    then
        bashtpl:build "${BASHTPL_INPUT_2}" "${BASHTPL_OUTPUT_2}"
    fi
    if [ ! -z "${BASHTPL_INPUT_3}" ] && [ ! -z "${BASHTPL_OUTPUT_3}" ]
    then
        bashtpl:build "${BASHTPL_INPUT_3}" "${BASHTPL_OUTPUT_3}"
    fi
    if [ ! -z "${BASHTPL_INPUT_4}" ] && [ ! -z "${BASHTPL_OUTPUT_4}" ]
    then
        bashtpl:build "${BASHTPL_INPUT_4}" "${BASHTPL_OUTPUT_4}"
    fi
    if [ ! -z "${BASHTPL_INPUT_5}" ] && [ ! -z "${BASHTPL_OUTPUT_5}" ]
    then
        bashtpl:build "${BASHTPL_INPUT_5}" "${BASHTPL_OUTPUT_5}"
    fi
}

bashtpl:update() {
    if [ ! -z "${BASHTPL_INPUT_1}" ] && [ ! -z "${BASHTPL_OUTPUT_1}" ]
    then
        bashtpl:build_prompt "${BASHTPL_INPUT_1}" "${BASHTPL_OUTPUT_1}"
    fi
    if [ ! -z "${BASHTPL_INPUT_2}" ] && [ ! -z "${BASHTPL_OUTPUT_2}" ]
    then
        bashtpl:build_prompt "${BASHTPL_INPUT_2}" "${BASHTPL_OUTPUT_2}"
    fi
    if [ ! -z "${BASHTPL_INPUT_3}" ] && [ ! -z "${BASHTPL_OUTPUT_3}" ]
    then
        bashtpl:build_prompt "${BASHTPL_INPUT_3}" "${BASHTPL_OUTPUT_3}"
    fi
    if [ ! -z "${BASHTPL_INPUT_4}" ] && [ ! -z "${BASHTPL_OUTPUT_4}" ]
    then
        bashtpl:build_prompt "${BASHTPL_INPUT_4}" "${BASHTPL_OUTPUT_4}"
    fi
    if [ ! -z "${BASHTPL_INPUT_5}" ] && [ ! -z "${BASHTPL_OUTPUT_5}" ]
    then
        bashtpl:build_prompt "${BASHTPL_INPUT_5}" "${BASHTPL_OUTPUT_5}"
    fi
}

task:gentpl() {
    bashtpl:update
}
