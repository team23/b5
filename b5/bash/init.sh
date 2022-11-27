#!/usr/bin/env bash

# Initialize error handling
set -o errexit
set -o errtrace
set -o pipefail
trap 'b5:error_exit' ERR

# Font colors
B5_FONT_GREEN='\033[00;32m'
B5_FONT_YELLOW='\033[00;33m'
B5_FONT_RED='\033[00;31m'
B5_FONT_RESTORE='\033[0m'
