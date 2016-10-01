#!/bin/bash

cd TLE

wget  --post-data='identity=asavari.limaye@gmail.com&password=2016AACNITK2017&query=https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/'${1}'/orderby/ORDINAL asc/limit/1/format/3le/metadata/false' --cookies=on --keep-session-cookies --save-cookies=cookies.txt 'https://www.space-track.org/ajaxauth/login' -O $1.txt
