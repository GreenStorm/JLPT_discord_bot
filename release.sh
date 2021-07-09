#!/bin/sh
fc-list | grep 'IPA'
mkdir -p ~/.local/share/fonts
cp ./fonts/ipaexg.ttf ~/.local/share/fonts
fc-cache -f -v
fc-list | grep 'IPA'
exit 0;