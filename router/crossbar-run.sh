#!/bin/bash

exec docker run \
    -v $PWD:/node \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -p 8094:80 \
    -u 0 --rm \
    --name=crossbar -it \
    crossbario/crossbar --loglevel info


# -v /etc/letsencrypt:/etc/letsencrypt \
