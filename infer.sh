#!/bin/sh
cd "$('dirname' '--' "${0}")"
cog predict -i 'input_file_background=@/home/ubuntu/bkg.jpg' 'input_file_subject=@/home/ubuntu/subject.png'
exit '0'
