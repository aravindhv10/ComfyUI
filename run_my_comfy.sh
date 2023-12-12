#!/bin/sh
. "${HOME}/dbnew/bin/activate"
cd "${HOME}/GITHUB/aravindhv10/ComfyUI"
echo 'http://127.0.0.1:8188' | xc
python3 './main.py'
