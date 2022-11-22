#!/bin/sh
basedir=$(dirname $0)
echo $basedir
cp $basedir/../requirements.txt $basedir/
docker build -t 'ndgnuh/torch-dev-env' $basedir/
rm $basedir/requirements.txt
