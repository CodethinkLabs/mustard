#!/usr/bin/python
#
# Copyright (C) 2012-2013 Codethink Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
        project_code = environ.get('MUSTARD_PROJECT_CODE', '')
        base_url = environ.get('MUSTARD_BASE_URL', '')

        sys.path.append(server_path)
        os.chdir(os.path.dirname(__file__))

        import mustard
        mustard.renderer.App().run([
            '-p', project_path,
            '-j', plantuml_jar,
            '-s', 'cherrypy',
            '--auth', auth,
            '--auth-server=%s' % auth_server,
            '--base-url', base_url,
            '--config', config_file,
            '--project-code', project_code,
            ])

        app = bottle.default_app()

    return app(environ, start_response)
