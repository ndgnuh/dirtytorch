#!/bin/bash
args=""
if [ -d $HOME/.deepface ]; then
	args="$args --mount type=bind,source=$HOME/.deepface/,target=/home/dev/.deepface"
fi
if [ -d $HOME/.cache ]; then
	args="$args --mount type=bind,source=$HOME/.cache/,target=/home/dev/.cache"
fi
if [ -e /dev/video0 ]; then
	args="$args --device /dev/video0"
fi
if [ -f $HOME/.Xauthority ]; then
	args=$args' --volume '"$HOME/.Xauthority:/home/dev/.Xauthority"
fi
echo "$args"
docker run -it --rm $@ \
	--mount type=bind,source=/dev,target=/dev \
	--mount type=bind,source=/sys,target=/sys \
	--mount type=bind,source=/proc,target=/proc \
	--mount type=bind,source=/tmp/,target=/tmp \
	--mount type=bind,source=$PWD,target=/home/dev/working \
	--network host \
	--user $(id -u):$(id -g) \
	--gpus all \
	--env DISPLAY=$DISPLAY \
	$args \
	"ndgnuh/torch-dev-env" 

	# --mount type=bind,source=$HOME/.deepface,target=/home/dev/.deepface \
	# --volume "/tmp/.X11-unix:/tmp/.X11-unix" \
	# --volume "$HOME/.Xauthority:/home/dev/.Xauthority" \
	# --volume "$PWD/:/home/dev/working" \
	# --volume "$HOME/.cache:/home/dev/.cache" \
	# --volume "$HOME/.deepface:/home/dev/.deepface" \ 
# --cpus "all" \
# --gpus "all" \
	# --env DISPLAY=$DISPLAY \
	# --network host \
	# --entrypoint bash \
