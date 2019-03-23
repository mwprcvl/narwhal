#!/usr/bin/env bash

# create some runtime data on the container
echo "$(date +%Y-%m-%d)" > runtime.txt

# argument given is keyword to run app or otherwise
case "$1" in
    app)
        exec python app.py
        ;;
    default)
        echo "Hello, world, from bash."
        cat runtime.txt
        ;;
    *)
        exec "$@"
        ;;
esac
