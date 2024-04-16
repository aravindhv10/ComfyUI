#!/bin/sh
cd "$('dirname' '--' "${0}")"
sudo cog predict -i 'input_file_background=@/home/ubuntu/bkg.jpg' -i  'input_file_subject=@/home/ubuntu/subject.png'
exit '0'
