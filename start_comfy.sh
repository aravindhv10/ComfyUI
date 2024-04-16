#!/bin/sh
cd "$('dirname' '--' "${0}")"
python './main.py' --port 8188 --listen
exit '0'
