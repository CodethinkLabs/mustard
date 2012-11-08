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
    'reload': False,
}


class App(cliapp.Application):

    def __init__(self):
        cliapp.Application.__init__(self)

        self.states = {}
        self.content = {}
        self.uml = {}

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
        self.settings.boolean(['reload', 'r'],
                              'Reload whenever the mustard code changes',
                              default=defaults['reload'])

    def resolve_state(self, stateid):
        try:
            stateid = self.runcmd(['git', 'rev-list', '-n1', stateid],
                                  cwd=self.settings['project'])
            return stateid.split()[0]
        except:
            return stateid

    def render_repository(self, state, view):
        try:
            if state == 'UNCOMMITTED':
                project_state = mustard.state.State(
                        self, self.settings['project'], state)
                repo = mustard.repository.Repository(project_state, self.settings)
                return bottle.template(view, repository=repo)
            else:
                commit = self.resolve_state(state)
                content_id = (commit, view)

                if not content_id in self.content:
                    if not commit in self.states:
                        project_state = mustard.state.State(
                                self, self.settings['project'], state)
                        repo = mustard.repository.Repository(
                                project_state, self.settings)
                        self.states[commit] = repo
                    else:
                        repo = self.states[commit]
                    self.content[content_id] = bottle.template(view, repository=repo)

                return self.content[content_id]
        except cliapp.AppException, err:
            return bottle.template('error', error=err)

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')

        if not os.path.isdir(self.settings['project']):
            raise cliapp.AppException('Input project directory does not exist')

        states = {}
        cached_content = {}

        @route('/')
        def index():
            return bottle.redirect('/HEAD')

        @route('/favicon.ico')
        def favicon():
            return None

        @route('/<stateid>')
        def state_index(stateid):
            return self.render_repository(stateid, 'index')

        @route('/<stateid>/overview')
        def overview(stateid):
            return self.render_repository(stateid, 'overview')

        @route('/<stateid>/requirements')
        def requirements(stateid):
            return self.render_repository(stateid, 'requirements')

        @route('/<stateid>/architectures')
        def architectures(stateid):
            return self.render_repository(stateid, 'architectures')

        @route('/<stateid>/components')
        def components(stateid):
            return self.render_repository(stateid, 'components')

        @route('/<stateid>/tags')
        def tags(stateid):
            return self.render_repository(stateid, 'tags')

        @route('/<stateid>/work-items')
        def work_items(stateid):
            return self.render_repository(stateid, 'work-items')

        @route('/<stateid>/interfaces')
        def interfaces(stateid):
            return self.render_repository(stateid, 'interfaces')

        @route('/public/<filename>')
        def stylesheet(filename):
            public_dir = os.path.join(os.path.dirname(__file__),
                                      '..', 'views', 'public')
            return bottle.static_file(filename, root=public_dir)

        @route('/plantuml/<content:re:.*>')
        def plantuml(content):
            if not content in self.uml:
                uml = base64.b64decode(urllib.unquote(content))
                self.uml[content] = self.runcmd(
                        ["java", "-jar", self.settings['plantuml-jar'],
                         "-tpng", "-p"],
                        feed_stdin=uml)
            bottle.response.content_type = 'image/png'
            return self.uml[content]

        if self.settings['run-bottle']:
            bottle.run(host='0.0.0.0',
                       port=self.settings['port'],
                       server=self.settings['server'],
                       reloader=self.settings['reload'])
