#!/usr/bin/env bash
set +ex

URL="http://www.st-minutiae.com/resources/scripts/scripts_tng.zip"
FILENAME="file.zip"
mkdir ./data && \
cd ./data && \
curl -sS ${URL} > ${FILENAME} && \
unzip ${FILENAME} && \
rm ${FILENAME}
