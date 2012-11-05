#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

import mustard


def application(environ, start_response):
    server_path = environ['MUSTARD_SERVER_PATH']
    project_path = environ['MUSTARD_PROJECT_PATH']

    sys.path = [server_path] + sys.path
    os.chdir(os.path.dirname(__file__))

    app = mustard.renderer.App().run(['-p', project_path])

    return bottle.default_app().wsgi(environent, start_response)
