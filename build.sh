#!/bin/sh
cd "$('dirname' '--' "${0}")"
sudo cog build -t simple_bkg_swap
exit '0'
