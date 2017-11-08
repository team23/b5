#!/usr/bin/env bash

b5:warn() {
    echo -e "${B5_FONT_YELLOW}${1:-}${B5_FONT_RESTORE}"
}

b5:error() {
    echo -e "${B5_FONT_RED}${1:-}${B5_FONT_RESTORE}"
}

b5:abort() {
    b5:error "$@"
    exit 1
}

b5:error_exit() {
    local err=$?
    set +o xtrace
    local code="${1:-1}"
    echo
    echo "Error in ${BASH_SOURCE[1]}:${BASH_LINENO[0]}. '${BASH_COMMAND}' exited with status $err"
    # Print out the stack trace described by $function_stack
    if [ ${#FUNCNAME[@]} -gt 2 ]
    then
        echo "Call tree:"
        for ((i=1;i<${#FUNCNAME[@]}-1;i++))
        do
            echo " $i: ${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]} ${FUNCNAME[$i]}(...)"
        done
    fi
    echo "Exiting with status ${code}"
    echo -e "\n${B5_FONT_RED}Task failed, see error above${B5_FONT_RESTORE}"
    exit "${code}"
}

b5:function_exists() {
    local function="${1:-}"
    if [ -z "function" ]
    then
        b5:error "Usage: b5:function_exists <function_name>"
        return 254
    fi

    local type_result=$( type -t "${function}" )
    if [ "$type_result" == "function" ]
    then
        return 0
    else
        return 1
    fi
}

b5:help() {
    local taskname="${1:-}"
    if [ ! -z "$taskname" ]
    then
        if b5:function_exists "help:$taskname"
        then
            shift 1  # remove $taskname from $@
            help:$taskname "$@"
            return 0
        else
            b5:warn "No dedicated help found for ${taskname}"
            echo
        fi
    fi

    echo "b5 <task> <args>"
    echo "Tasks:"
    compgen -A function | sed -En 's/task:(.*)/\1/p' | cat -n
}

b5:run() {
    "$@"
    echo -e "\n${B5_FONT_GREEN}Task exited ok${B5_FONT_RESTORE}"
}
