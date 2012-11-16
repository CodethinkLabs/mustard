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

        self.repository = None
        self.state_cache = None
        raw_tree_cache = mustard.rawtree.Cache()
        self.element_tree_cache = mustard.elementtree.Cache(raw_tree_cache)

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

    def render_repository(self, state_id, view):
        state = self.state_cache.get(state_id)

        try:
            if state_id == 'UNCOMMITTED':
                raw_tree = mustard.rawtree.Tree(state)
                element_tree = mustard.elementtree.Tree(raw_tree)
                return bottle.template(view, tree=element_tree)
            else:
                content_id = (state, view)
                if not content_id in self.content:
                    element_tree = self.element_tree_cache.get(state)
                    self.content[content_id] = bottle.template(
                            view, tree=element_tree)
                return self.content[content_id]
        except cliapp.AppException, err:
            return bottle.template('error', error=err)

    def render_diff(self, state1, state2, view):
        state1 = self.state_cache.get(state1)
        state2 = self.state_cache.get(state2)

        try:
            if state1 == state2:
                raise cliapp.AppException('Need two different states')

            if state1.identifier == 'UNCOMMITTED':
                raw_tree1 = mustard.rawtree.Tree(state)
                element_tree1 = mustard.elementtree.Tree(raw_tree)
                element_tree2 = self.element_tree_cache.get(state2)

                return bottle.template(
                        'diff', tree=element_tree1, other_tree=element_tree2)
            else:
                content_id = (state1, state2, view)
                if not content_id in self.content:
                    tree1 = self.element_tree_cache.get(state1)
                    tree2 = self.element_tree_cache.get(state2)

                    self.content[content_id] = bottle.template(
                            'diff', tree=tree1, other_tree=tree2)
                else:
                    print 'using cached rendering of (%s, %s, %s)' % content_id
                return self.content[content_id]
        except cliapp.AppException, err:
            return bottle.template('error', error=err)

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')

        if not os.path.isdir(self.settings['project']):
            raise cliapp.AppException('Input project directory does not exist')

        self.repository = mustard.repository.Repository(
                self, self.settings['project'])
        self.state_cache = mustard.state.Cache(self, self.repository)

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

        @route('/<stateid>/integration-strategies')
        def integration_strategies(stateid):
            return self.render_repository(stateid, 'integration-strategies')

        @route('/<stateid>/tests')
        def tests(stateid):
            return self.render_repository(stateid, 'tests')

        @route('/<stateid>/history')
        def history(stateid):
            return self.render_repository(stateid, 'history')

        @route('/<stateid>/diff')
        def diff(stateid):
            return self.render_repository(stateid, 'diff')

        @route('/<state1>/diff/<state2>')
        def diff(state1, state2):
            return self.render_diff(state1, state2, 'diff')

        @route('/public/<filename>')
        def public(filename):
            public_dir = os.path.join(os.path.dirname(__file__),
                                      '..', 'views', 'public')
            return bottle.static_file(filename, root=public_dir)

        @route('/<stateid>/files/<filename:re:.*>')
        def file(stateid, filename):
            path = os.path.join('files/%s' % filename)
            state = self.state_cache.get(stateid)
            content_id = (state, 'files', path)
            try:
                if not content_id in self.content:
                    self.content[content_id] = state.read(path)
                return self.content[content_id]
            except Exception, err:
                bottle.response.status = 404
                return bottle.template('error', error=err)

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
