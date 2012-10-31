# Copyright (C) 2012 Codethink Limited


import bottle
import cliapp
import os

import mustard


defaults = {
    'port': 8080
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

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')
        
        project = self.settings['project']
        if not os.path.isdir(project):
            raise cliapp.AppException('Input project directory does not exist')

        app = bottle.Bottle()

        @app.get('/')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('index', repository=repository)

        @app.get('/requirements')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('requirements', repository=repository)

        @app.get('/architectures')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('architectures', repository=repository)

        @app.get('/components')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('components', repository=repository)

        @app.get('/tags')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('tags', repository=repository)

        @app.get('/work-items')
        def index():
            repository = mustard.repository.Repository(project)
            return bottle.template('work-items', repository=repository)

        @app.get('/public/<filename>')
        def stylesheet(filename):
            return bottle.static_file(filename, root='views/public')
        
        bottle.run(app, host='0.0.0.0', port=self.settings['port'],
                   reloader=True)
