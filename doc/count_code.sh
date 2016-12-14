#!/bin/bash

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/

cloc ../ --exclude-ext=xml --exclude-dir=json

