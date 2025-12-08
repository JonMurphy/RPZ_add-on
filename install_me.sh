#!/usr/bin/env bash

fileName="$1"

# Check for mandatory filename argument
[[ ! -f "${fileName}" ]] && echo "Usage: $0 /PATH/FILENAME" && exit 1

cd /opt/pakfire/tmp/

curl --silent --show-error --location \
  --url https://github.com/JonMurphy/RPZ/raw/refs/heads/main/"${fileName}.tar" \
  --output "${fileName}"

tar --extract --verbose --file="${fileName}"

ls -l

/bin/cp --verbose ROOTFILES /opt/pakfire/db/rootfiles/rpz  # need force here??

NAME=rpz ./install.sh
# -or-
NAME=rpz ./install.sh
