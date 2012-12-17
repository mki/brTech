#!/bin/bash

#Если python установлен не в системные директории
#PATH=$PATH:/opt/python266/bin:/opt/python266
#export PATH

#Если не установлен pip и virtualenv
#apt-get install python-pip
#pip install virtualenv

#Если ругается при pip install lxml
#yum install libxml2-devel libxslt-devel

virtualenv .env --no-site-packages -p python2.7
./.env/bin/easy_install-2.7 pip
./.env/bin/pip-2.7 install -r requirements.txt
