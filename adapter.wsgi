#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

def application(environ, start_response):
    server_path = environ['MUSTARD_SERVER_PATH']
    project_path = environ['MUSTARD_PROJECT_PATH']

    sys.path.append(server_path)
    os.chdir(os.path.dirname(__file__))

    print server_path
    print os.path.dirname(__file__)

    import mustard
    app = mustard.renderer.App().run(['-p', project_path])

    return bottle.default_app()(environ, start_response)
