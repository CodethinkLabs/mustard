#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

print os.environ

server_path = os.environ['MUSTARD_SERVER_PATH']
project_path = os.environ['MUSTARD_PROJECT_PATH']

sys.path = [server_path] + sys.path
os.chdir(os.path.dirname(__file__))

import mustard.renderer

app = mustard.renderer.App().run(['-p', project_path])
application = bottle.default_app()
