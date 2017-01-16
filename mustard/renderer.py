# Copyright (C) 2012-2016 Codethink Limited
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


import base64
import bottle
import cliapp
import mimetypes
import os
import pkgutil
import urllib
import zlib

from bottle import route

import mustard


defaults = {
    'auth': 'none',
    'base-url': '/',
    'port': 8080,
    'plantuml-jar': '/usr/local/share/plantuml.jar',
    'reload': False,
    'auto-fetch': False,
    'run-bottle': False,
    'server': 'wsgiref',
}


class App(cliapp.Application):

    def __init__(self):
        cliapp.Application.__init__(self)

        self.repository = None

        self.auth = None
        self.state_cache = None
        raw_tree_cache = mustard.rawtree.Cache()
        self.element_tree_cache = mustard.elementtree.Cache(raw_tree_cache)

        self.content = {}
        self.uml = {}

        # load available authentication mechanisms
        self.auth_mechanisms = {}
        from mustard import auth
        auth_path = os.path.dirname(auth.__file__)
        for module_loader, name, _ in pkgutil.iter_modules([auth_path]):
            try:
                self.auth_mechanisms[name] = \
                    module_loader.find_module(name).load_module(name)
            except ImportError:
                pass

    def add_settings(self):
        self.settings.string(['auth'],
                             'Authentication mechanism '
                             '(%s; default: %s)' % (
                                 ', '.join(self.auth_mechanisms.iterkeys()),
                                 defaults['auth'],
                                 ),
                             metavar='MECHANISM',
                             default=defaults['auth'])
        self.settings.string(['auth-server'],
                             'Authentication server to use',
                             metavar='SERVER')
        self.settings.string(['auth-user'],
                             'Authentication lookup user (optional)',
                             metavar='USER')
        self.settings.string(['auth-password'],
                             'Authentication lookup password (optional)',
                             metavar='PASSWORD')
        self.settings.boolean(['auto-fetch'],
                              'Automatically fetch the source repo from its '
                              'remotes periodically',
                              metavar='AUTOFETCH',
                              default=defaults['auto-fetch'])
        self.settings.string(['base-url'],
                             'Base URL to the Mustard service (optional)',
                             metavar='URL',
                             default=defaults['base-url'])
        self.settings.integer(['port'],
                              'Port to listen on',
                              metavar='PORTNUM',
                              default=defaults['port'])
        self.settings.string(['project', 'p'],
                             'Location of the input project',
                             metavar='DIR')
        self.settings.string(['project-code'],
                             'Project code (e.g. XYZ)',
                             metavar='XYZ')
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
        try:
            if state_id == 'admin':
                raise cliapp.AppException(
                    'Browsing this branch is not permitted')

            state = self.state_cache.get(state_id)

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
        except mustard.MustardError as err:
            return bottle.template('treeerror', error=err)
        except cliapp.AppException as err:
            return bottle.template('error', error=err)

    def render_diff(self, state1, state2, view):
        try:
            if state1 == 'admin' or state2 == 'admin':
                raise cliapp.AppException(
                    'Browsing this branch is not permitted')

            state1 = self.state_cache.get(state1)
            state2 = self.state_cache.get(state2)

            if state1 == state2:
                raise cliapp.AppException('Need two different states')

            if state1.identifier == 'UNCOMMITTED':
                raw_tree1 = mustard.rawtree.Tree(state1)
                element_tree1 = mustard.elementtree.Tree(raw_tree1)
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
                    print ('using cached rendering of (%s, %s, %s)' % content_id)
                return self.content[content_id]
        except cliapp.AppException as err:
            return bottle.template('error', error=err)

    def render_export(self, stateid, view, forms=None):
        try:
            if stateid == 'admin':
                raise cliapp.AppException(
                    'Browsing this branch is not permitted')

            state = self.state_cache.get(stateid)

            raw_tree = mustard.rawtree.Tree(state)
            element_tree = mustard.elementtree.Tree(raw_tree)
            return bottle.template(
                view, tree=element_tree, forms=forms,
                elements=mustard.elementfactory.element_descriptions)
        except cliapp.AppException as err:
            return bottle.template('error', error=err)

    def process_args(self, args):
        if not self.settings['project']:
            raise cliapp.AppException('Input project directory not defined')

        if not os.path.isdir(self.settings['project']):
            raise cliapp.AppException('Input project directory does not exist')

        try:
            self.repository = mustard.repository.Repository(
                self, self.settings['project'])
        except KeyError:
            raise cliapp.AppException('Input project directory is not a git directory')

        if not self.settings['auth'] in self.auth_mechanisms:
            raise cliapp.AppException(
                'Unsupported authentication mechanism: %s' %
                self.settings['auth'])

        auth_module = self.auth_mechanisms[self.settings['auth']]
        self.auth = auth_module.Authenticator(
                self, self.settings, self.repository)

        base_url = self.settings['base-url']
        self.base_url = base_url

        self.state_cache = mustard.state.Cache(self.base_url, self.repository)

        print ('base url: %s' % self.base_url)

        @route('/')
        @self.auth.protected
        def index():
            print ('redirect to %s' % os.path.join(self.base_url, 'HEAD/'))
            return bottle.redirect(os.path.join(self.base_url, 'HEAD/'))

        @route('/favicon.ico')
        def favicon():
            return None

        @route('/<stateid>')
        @self.auth.protected
        def state_redirect(stateid):
            return bottle.redirect(
                os.path.join(self.base_url, '%s/' % stateid))

        @route('/<stateid>/')
        @self.auth.protected
        def state_index(stateid):
            return self.render_repository(stateid, 'index')

        @route('/<stateid>/overview')
        @self.auth.protected
        def overview(stateid):
            return self.render_repository(stateid, 'overview')

        @route('/<stateid>/requirements')
        @self.auth.protected
        def requirements(stateid):
            return self.render_repository(stateid, 'requirements')

        # only exists for backwards-compatibility, /architecture is the new way
        @route('/<stateid>/architectures')
        @self.auth.protected
        def old_architectures(stateid):
            return self.render_repository(stateid, 'components')

        # only exists for backwards-compatibility, /architecture is the new way
        @route('/<stateid>/components')
        @self.auth.protected
        def old_components(stateid):
            return self.render_repository(stateid, 'components')

        @route('/<stateid>/architecture')
        @self.auth.protected
        def architecture(stateid):
            return self.render_repository(stateid, 'components')

        @route('/<stateid>/tags')
        @self.auth.protected
        def tags(stateid):
            return self.render_repository(stateid, 'tags')

        @route('/<stateid>/work-items')
        @self.auth.protected
        def work_items(stateid):
            return self.render_repository(stateid, 'work-items')

        @route('/<stateid>/interfaces')
        @self.auth.protected
        def interfaces(stateid):
            return self.render_repository(stateid, 'interfaces')

        @route('/<stateid>/integration-strategies')
        @self.auth.protected
        def integration_strategies(stateid):
            return self.render_repository(stateid, 'integration-strategies')

        @route('/<stateid>/verification-criteria')
        @self.auth.protected
        def verification_criteria(stateid):
            return self.render_repository(stateid, 'verification-criteria')

        @route('/<stateid>/history')
        @self.auth.protected
        def history(stateid):
            return self.render_repository(stateid, 'history')

        @route('/<stateid>/diff')
        @self.auth.protected
        def diff(stateid):
            return self.render_repository(stateid, 'diff')

        @route('/<state1>/diff/<state2>')
        @self.auth.protected
        def diff_states(state1, state2):
            return self.render_diff(state1, state2, 'diff')

        @route('/<stateid>/export')
        @self.auth.protected
        def export(stateid):
            return self.render_export(stateid, 'export')

        @route('/<stateid>/export', method='POST')
        @self.auth.protected
        def perform_export(stateid):
            return self.render_export(
                stateid, 'export-html', bottle.request.forms)

        @route('/public/<filename>')
        @self.auth.protected
        def public(filename):
            public_dir = os.path.join(os.path.dirname(__file__),
                                      '..', 'views', 'public')
            return bottle.static_file(filename, root=public_dir)

        @route('/<stateid>/files/<filename:re:.*>')
        @self.auth.protected
        def file(stateid, filename):
            if stateid == 'admin':
                raise cliapp.AppException(
                    'Browsing this branch is not permitted')

            path = os.path.join('files/%s' % filename)
            state = self.state_cache.get(stateid)
            content_id = (state, 'files', path)
            try:
                if not content_id in self.content:
                    self.content[content_id] = state.read(path)

                mime_type, encoding = mimetypes.guess_type(filename)
                bottle.response.set_header('Content-Type', mime_type)
                bottle.response.set_header('Content-Encoding', encoding)

                return self.content[content_id]
            except Exception as err:
                bottle.response.status = 404
                return bottle.template('error', error=err)

        @route('/plantuml/<content:re:.*>')
        @self.auth.protected
        def plantuml(content):
            if not content in self.uml:
                uml = zlib.decompress(
                    base64.urlsafe_b64decode(urllib.unquote(content)))
                self.uml[content] = self.runcmd(
                        ["java", "-jar", self.settings['plantuml-jar'],
                         "-tpng", "-p"], feed_stdin=uml)
            bottle.response.content_type = 'image/png'
            return self.uml[content]

        if self.settings['run-bottle']:
            bottle.run(host='0.0.0.0',
                       port=self.settings['port'],
                       server=self.settings['server'],
                       reloader=self.settings['reload'])
