#!/bin/sh
cd "$('dirname' '--' "${0}")"
NAME='simple_bkg_swap'

sudo docker run \
    '--gpus' 'all' \
    '-it' \
    '--runtime=nvidia' \
    '--shm-size=16gb' \
    '--publish' '8188:8188' \
    "${NAME}" \
    '/bin/bash' \
;
exit '0'
