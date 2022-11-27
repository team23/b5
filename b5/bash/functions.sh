#!/usr/bin/env bash

# Core functions

b5:warn() {
    echo -e "${B5_FONT_YELLOW}${1:-}${B5_FONT_RESTORE}" >&2
}

b5:error() {
    echo -e "${B5_FONT_RED}${1:-}${B5_FONT_RESTORE}" >&2
}

b5:abort() {
    b5:error "$@" >&2
    exit 1
}

b5:error_exit() {
    local err=$?
    set +o xtrace
    local code="${1:-1}"
    echo
    #echo "Error in ${BASH_SOURCE[1]}:${BASH_LINENO[0]}. '${BASH_COMMAND}' exited with status $err"
    echo "Error: '${BASH_COMMAND}' exited with status $err"
    if [ ${_DEBUG_TRACEBACK:-0} -gt 0 ]
    then
        # Print out the stack trace described by $function_stack
        if [ ${#FUNCNAME[@]} -gt 2 ]
        then
            echo "Call tree:"
            for ((i=1;i<${#FUNCNAME[@]}-1;i++))
            do
                #echo " $i: ${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]} ${FUNCNAME[$i]}(...)"
                echo " $i: ${FUNCNAME[$i]}(...)"
            done
        fi
    fi
    echo "b5 exiting with status ${code}"
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

b5:bin_exists() {
    which "${1:-}" > /dev/null && return 0 || return 1
}

b5:help() {
    local arg="${1:-}"

    case $arg in
        "--tasks")
            compgen -A function | sed -En 's/task:(.*)/\1/p'
            ;;
        "--usage")
            echo "Usage: b5 <task> [args]"
            ;;
        *)
            local taskname="$arg"
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

            echo "Usage: b5 <task> <args>"
            echo
            echo "Tasks:"
            compgen -A function | sed -En 's/task:(.*)/\1/p' | cat -n
            echo
            ;;
    esac
}

b5:run() {
    "$@"
    # echo -e "\n${B5_FONT_GREEN}Task exited ok${B5_FONT_RESTORE}"
}

# Config

b5:config_get() {
    if [ -z "${1:-}" ]
    then
        echo "Usage: config_get <variable_name> [default]"
        exit 1
    fi

    local config_name="CONFIG_$1"
    local default="$2"
    eval "echo \"\${${config_name}:-${default}}\""
}

# Legacy support

b5:module_load() {
    echo -e "${B5_FONT_YELLOW}Seems like you are using the old module loading mechanism!${B5_FONT_RESTORE}"
    echo -e "${B5_FONT_YELLOW}It has been made obsolete and will not be supported in the${B5_FONT_RESTORE}"
    echo -e "${B5_FONT_YELLOW}future.${B5_FONT_RESTORE}"
    echo -e ""
    echo -e "${B5_FONT_YELLOW}You may reenable using 'b5:module_load' and all legacy modules${B5_FONT_RESTORE}"
    echo -e "${B5_FONT_YELLOW}by adding the 'legacy' module to your config.yml${B5_FONT_RESTORE}"
    echo -e ""
    echo -e "${B5_FONT_YELLOW}Example config.yml:${B5_FONT_RESTORE}"
    echo -e "${B5_FONT_YELLOW}modules:${B5_FONT_RESTORE}"
    echo -e "${B5_FONT_YELLOW}  legacy:${B5_FONT_RESTORE}"
    echo -e ""
    exit 1
}
