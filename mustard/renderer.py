# Copyright (C) 2012 Codethink Limited


import bottle
import cliapp
import os
import urllib
import base64

import mustard


defaults = {
    'port': 8080,
    'plantuml-jar': '/usr/local/share/plantuml.jar',
}


class App(cliapp.Application):

    def add_settings(self):
        self.settings.integer(['port'],
                              'Port to listen on',
                              metavar='PORTNUM',
                              default=defaults['port'])
        self.settings.string(['project', 'p'],
                             'Location of the input project',
                             metavar='DIR')
        self.settings.string(['plantuml-jar', 'j'],
                             'Path to the PlantUML JAR file',
                             metavar='JARPATH',
                             default=defaults['plantuml-jar'])

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')
        
        project = self.settings['project']
        if not os.path.isdir(project):
            raise cliapp.AppException('Input project directory does not exist')

        app = bottle.Bottle()

        @app.get('/')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('overview', repository=repository)

        @app.get('/requirements')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('requirements', repository=repository)

        @app.get('/architectures')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('architectures', repository=repository)

        @app.get('/components')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('components', repository=repository)

        @app.get('/tags')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('tags', repository=repository)

        @app.get('/work-items')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('work-items', repository=repository)

        @app.get('/interfaces')
        def index():
            repository = mustard.repository.Repository(project, self.settings)
            return bottle.template('interfaces', repository=repository)

        @app.get('/public/<filename>')
        def stylesheet(filename):
            return bottle.static_file(filename, root='views/public')

        @app.get('/plantuml/<content:re:.*>')
        def plantuml(content):
            uml = base64.b64decode(urllib.unquote(content))
            image = self.runcmd(["java", "-jar", self.settings['plantuml-jar'],
                                 "-tpng", "-p"], feed_stdin=uml)
            bottle.response.content_type = 'image/png'
            return image
        
        bottle.debug(True)
        bottle.run(app, host='0.0.0.0', port=self.settings['port'],
                   reloader=True)
