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
        
        bottle.run(app, host='0.0.0.0', port=self.settings['port'],
                   reloader=True)
