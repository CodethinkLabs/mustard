#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

app = None

def application(environ, start_response):
    if not self.app:
        server_path = environ['MUSTARD_SERVER_PATH']
        project_path = environ['MUSTARD_PROJECT_PATH']
        plantuml_jar = environ['MUSTARD_PLANTUML_JAR']

        sys.path.append(server_path)
        os.chdir(os.path.dirname(__file__))

        import mustard
        mustard.renderer.App().run([
            '-p', project_path,
            '-j', plantuml_jar,
            '-s', 'cherrypy',
            ])

        self.app = bottle.default_app()

    return self.app(environ, start_response)
