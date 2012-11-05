#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

print os.environ

sys.path = [server_path] + sys.path
os.chdir(os.path.dirname(__file__))

import mustard.renderer

def application(environ, start_response):
    os.environ['MUSTARD_SERVER_PATH'] = environ['MUSTARD_SERVER_PATH']
    os.environ['MUSTARD_PROJECT_PATH'] = environ['MUSTARD_PROJECT_PATH']
    app = mustard.renderer.App().run(['-p', project_path])
    return bottle.default_app().wsgi(environent, start_response)
