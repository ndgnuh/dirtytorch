#!/bin/sh
# name="torch-dev-env"
# count_container=$(docker ps --filter name="$name" -a | wc -l)
# if [ $count_container -le 1 ]; then
		# --name "$name" \
	docker run -it \
		--rm \
		--volume /tmp/.X11-unix:/tmp/.X11-unix \
		--volume $HOME/.Xauthority:/home/dev/.Xauthority \
		--volume $PWD/:/home/dev/working \
		--volume $HOME/.cache:/home/dev/.cache \
		--volume $HOME/.deepface:/home/dev/.deepface \ # Deep face cache
		--device /dev/video0:/dev/video0 \
		--gpus all \
		--env DISPLAY=$DISPLAY \
		--network host \
		--entrypoint bash \
		"ndgnuh/torch-dev-env" 
		# --volume /dev:/dev \
		# --volume /sys:/sys \
		# --volume /proc:/proc \
	#
# else
# 	docker start -it $name bash
# fi
