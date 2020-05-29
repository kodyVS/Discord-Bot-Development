#!/bin/bash
CONTAINER_NAME="pg_bot"
grep_container=$(docker images | grep -i "${CONTAINER_NAME}")
len_str=${#grep_container}

check_container(){
	if [ $len_str -ne 0 ]
		then
			return 0
		else
			return 1
	fi
}

build_and_run(){
	docker build -t pg_bot . &&
	docker run -itd --name pg_bot -v $(pwd):/app pg_bot
}


if check_container
	then docker start pg_bot
	else build_and_run 
fi

