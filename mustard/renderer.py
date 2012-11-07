# Copyright (C) 2012 Codethink Limited


import bottle
import cliapp
import os
import urllib
import base64

import mustard

from bottle import route


defaults = {
    'port': 8080,
    'plantuml-jar': '/usr/local/share/plantuml.jar',
    'run-bottle': False,
    'server': 'wsgiref',
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
        self.settings.boolean(['run-bottle', 'b'],
                              'Run the bottle web application',
                              default=defaults['run-bottle'])
        self.settings.string(['server', 's'],
                             'Run bottle in a specific server (e.g. cherrypy)',
                             default=defaults['server'])

    def resolve_state(self, project, stateid):
        if stateid != 'UNCOMMITTED':
            try:
                stateid = self.runcmd(['git', 'rev-list', '-n1', stateid],
                                      cwd=project)
                stateid = stateid.split()[0]
            except:
                pass
        return stateid

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')
        
        project = self.settings['project']
        if not os.path.isdir(project):
            raise cliapp.AppException('Input project directory does not exist')

        states = {}

        @route('/')
        def index():
            return bottle.redirect('/HEAD')

        @route('/favicon.ico')
        def favicon():
            return None

        @route('/<stateid>')
        def state_index(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('index', repository=repository)

        @route('/<stateid>/overview')
        def overview(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('overview', repository=repository)

        @route('/<stateid>/requirements')
        def requirements(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('requirements', repository=repository)

        @route('/<stateid>/architectures')
        def architectures(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('architectures', repository=repository)

        @route('/<stateid>/components')
        def components(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('components', repository=repository)

        @route('/<stateid>/tags')
        def tags(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('tags', repository=repository)

        @route('/<stateid>/work-items')
        def work_items(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('work-items', repository=repository)

        @route('/<stateid>/interfaces')
        def interfaces(stateid):
            commit = self.resolve_state(project, stateid)
            if not commit in states:
                state = mustard.state.State(self, project, stateid)
                repository = mustard.repository.Repository(state, self.settings)
                states[commit] = repository
            else:
                repository = states[commit]
            return bottle.template('interfaces', repository=repository)

        @route('/public/<filename>')
        def stylesheet(filename):
            public_dir = os.path.join(os.path.dirname(__file__),
                                      '..', 'views', 'public')
            return bottle.static_file(filename, root=public_dir)

        @route('/plantuml/<content:re:.*>')
        def plantuml(content):
            uml = base64.b64decode(urllib.unquote(content))
            image = self.runcmd(["java", "-jar", self.settings['plantuml-jar'],
                                 "-tpng", "-p"], feed_stdin=uml)
            bottle.response.content_type = 'image/png'
            return image
        
        if self.settings['run-bottle']:
            bottle.run(host='0.0.0.0',
                       port=self.settings['port'],
                       server=self.settings['server'],
                       reloader=True)
