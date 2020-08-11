#! /bin/bash

if [[ $1 == "run" ]]; then
    # "compose run" automatically adds the --rm flag
    docker-compose run --rm "${@:2}"
else
    docker-compose "${@:1}"
fi