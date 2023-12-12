#!/bin/sh
get_repo(){
    DIR_REPO="${HOME}/GITHUB/$('echo' "${1}" | 'sed' 's/^git@github.com://g ; s@^https://github.com/@@g ; s@.git$@@g' )"
    DIR_BASE="$('dirname' '--' "${DIR_REPO}")"
    mkdir -pv "${DIR_BASE}"
    cd "${DIR_BASE}"
    git clone "${1}"
    cd "${DIR_REPO}"
    git pull
    git submodule update --recursive --init
}

get_repo 'https://github.com/comfyanonymous/ComfyUI.git'

get_repo 'https://github.com/ltdrdata/ComfyUI-Manager.git'
ln -vfs -- "$(realpath .)" "${HOME}/GITHUB/aravindhv10//ComfyUI/custom_nodes/"

get_repo 'https://github.com/BlenderNeko/ComfyUI_ADV_CLIP_emb.git'
ln -vfs -- "$(realpath .)" "${HOME}/GITHUB/aravindhv10//ComfyUI/custom_nodes/"

get_repo 'https://github.com/TRI3D-LC/tri3d-comfyui-nodes.git'
ln -vfs -- "$(realpath .)" "${HOME}/GITHUB/aravindhv10//ComfyUI/custom_nodes/"

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/vae/vae-ft-mse-840000-ema-pruned.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/controlnet/control_v11p_sd15_openpose_fp16.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/controlnet/control_v11p_sd15_openpose_fp16.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/controlnet/control_v11p_sd15_canny_fp16.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/controlnet/control_v11p_sd15_canny_fp16.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/checkpoints/Realistic_Vision_V5.1.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/checkpoints/Realistic_Vision_V5.1.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/controlnet/control_v11p_sd15_inpaint_fp16.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/controlnet/control_v11p_sd15_inpaint_fp16.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/controlnet/control_v11p_sd15_lineart_fp16.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/controlnet/control_v11p_sd15_lineart_fp16.safetensors" \
;

ln -vfs -- \
    "${HOME}/GITHUB/comfyanonymous/ComfyUI/models/controlnet/control_v11f1e_sd15_tile_fp16.safetensors" \
    "${HOME}/GITHUB/aravindhv10/ComfyUI/models/controlnet/control_v11f1e_sd15_tile_fp16.safetensors" \
;
