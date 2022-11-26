#!/bin/sh
basedir=$(dirname $0)
docker build -t 'ndgnuh/torch-dev-env' $basedir/
