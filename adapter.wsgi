#!/usr/bin/python
#
# Copyright (C) 2012 Codethink Limited


import os
import sys
import bottle

app = None

def application(environ, start_response):
    global app

    if not app:
        config_file = environ.get(
                'MUSTARD_CONFIG_FILE', '/home/mustard/.mustard.conf')
        auth = environ.get('MUSTARD_AUTH', 'git')
        auth_server = environ['MUSTARD_AUTH_SERVER']
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
            '--auth', auth,
            '--auth-server=%s' % auth_server,
            '--config', config_file,
            ])

        app = bottle.default_app()

    return app(environ, start_response)
