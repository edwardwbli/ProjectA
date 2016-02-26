#!/usr/bin/env python
# encoding: utf-8

from fabric.api import env,run,local,cd

env.hosts = ['root@120.24.178.213:22',] #ssh要用的参数， 默认端口22

env.password = 'Lwb8930545@#$'

def rungunicorn():
    
    with cd('~/simple_wiki/'):
        run("nohup gunicorn -w4 -b0.0.0.0:8000 simple_wiki.wsgi &")

def runps():
    run("ps -fA | grep work")
