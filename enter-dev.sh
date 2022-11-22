#!/bin/sh
docker run -it \
	--name "torch-dev-env" \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume $HOME/.Xauthority:/home/dev/.Xauthority \
    --volume $PWD/:/home/dev/working \
    --volume /dev:/dev \
    --volume /sys:/sys \
    --volume /proc:/proc \
    --env DISPLAY=$DISPLAY \
    --network host \
    --entrypoint bash \
    "ndgnuh/torch-dev-env" 

