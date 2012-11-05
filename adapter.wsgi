#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

sys.path = ['/srv/genivi.baserock.com/'] + sys.path
os.chdir(os.path.dirname(__file__))

import mustard.renderer

application = bottle.default_app()
