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


import cliapp
import collections
import markdown
from markdown.treeprocessors import Treeprocessor
import base64
import zlib

import mustard

kind_aliases = {
    # Aliases to reduce wrist-strain for Mustardy people
    'r':      'requirement',
    'req':    'requirement',
    'a':      'component',
    'arch':   'component',
    'c':      'component',
    'comp':   'component',
    'i':      'interface',
    'iface':  'interface',
    'w':      'work-item',
    'work':   'work-item',
    't':      'tag',
    's':      'integration-strategy',
    'istrat': 'integration-strategy',
    'v':      'verification-criterion',
    'vcrit':  'verification-criterion',

    # Additional tag aliases for porting reasons (can be removed later)
    'architecture':  'component',
    'test':          'verification-criterion',
    'test-strategy': 'verification-criterion',
}

# Header level mapping for markdown
headermap = {
    'h1': 'h3',
    'h2': 'h4',
    'h3': 'h5',
    'h4': 'h6',
    'h5': 'h6',
    'h6': 'h6'
}


class HeaderDemotionProcessor(Treeprocessor):
    def run(self, element):
        for child in element:
            if child.tag in headermap:
                child.tag = headermap[child.tag]
            self.run(child)


class HeaderDemotionExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors['headerdemotion'] = HeaderDemotionProcessor(md)


md = markdown.Markdown(extensions=['extra', HeaderDemotionExtension()])


element_descriptions = {
  'requirement': {
    'title-plural':   'Requirements',
    'title-singular': 'Requirement',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True },
      { 'name': 'parent',       'title': 'Parent',       'default': True  },
      { 'name': 'mapped-to',    'title': 'Mapped To',    'default': True  },
      { 'name': 'path',         'title': 'Path',         'default': True },
    ]
  },
  'component': {
    'title-plural':   'Components',
    'title-singular': 'Component',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True },
      { 'name': 'parent',       'title': 'Parent',       'default': True  },
      { 'name': 'interfaces',   'title': 'Interfaces',   'default': True  },
      { 'name': 'vcrits',       'title': 'Verification Criteria',
        'default': True },
      { 'name': 'integration',  'title': 'Integration Strategies',
        'default': True },
      { 'name': 'work-items',   'title': 'Work Items',   'default': True  },
      { 'name': 'inherited',    'title': 'Inherited Requirements',
        'default': False },
      { 'name': 'requirements', 'title': 'Requirements', 'default': True  },
      { 'name': 'delegated',    'title': 'Delegated Requirements',
        'default': False },
      { 'name': 'path',         'title': 'Path',         'default': True },
    ]
  },
  'interface': {
    'title-plural':   'Interfaces',
    'title-singular': 'Interface',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True },
      { 'name': 'parent',       'title': 'Parent',       'default': True  },
      { 'name': 'work-items',   'title': 'Work Items',   'default': True  },
      { 'name': 'inherited',    'title': 'Inherited Requirements',
        'default': False },
      { 'name': 'requirements', 'title': 'Requirements', 'default': True  },
      { 'name': 'delegated',    'title': 'Delegated Requirements',
        'default': False },
      { 'name': 'path',         'title': 'Path',         'default': True },
    ]
  },
  'work-item': {
    'title-plural':   'Work Items',
    'title-singular': 'Work Item',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True  },
      { 'name': 'parents',      'title': 'Parents',      'default': True  },
      { 'name': 'inherited',    'title': 'Inherited Requirements',
        'default': False },
      { 'name': 'requirements', 'title': 'Requirements', 'default': True  },
      { 'name': 'path',         'title': 'Path',         'default': True  },
    ]
  },
  'tag': {
    'title-plural':   'Tags',
    'title-singular': 'Tag',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'used-by',      'title': 'Used By',      'default': True  },
    ]
  },
  'integration-strategy': {
    'title-plural':   'Integration Strategies',
    'title-singular': 'Integration Strategy',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True },
      { 'name': 'parent',       'title': 'Parent',       'default': True  },
      { 'name': 'vcrits',       'title': 'Verification Criteria',
        'default': True },
      { 'name': 'inherited',    'title': 'Inherited Requirements',
        'default': False },
      { 'name': 'requirements', 'title': 'Requirements', 'default': True  },
      { 'name': 'path',         'title': 'Path',         'default': True },
    ]
  },
  'verification-criterion': {
    'title-plural':   'Verification Criteria',
    'title-singular': 'Verification Criterion',
    'default': True,
    'fields': [
      { 'name': 'description',  'title': 'Description',  'default': True  },
      { 'name': 'tags',         'title': 'Tags',         'default': True },
      { 'name': 'parent',       'title': 'Parent',       'default': True  },
      { 'name': 'inherited',    'title': 'Inherited Requirements',
        'default': False },
      { 'name': 'requirements', 'title': 'Requirements', 'default': True  },
      { 'name': 'path',         'title': 'Path',         'default': True },
    ]
  },
}


class Element(object):

    def __init__(self, data):
        self.kind = data.get('kind', None)
        self.title = data.get('title', None)
        self.location = data.get('_location', '')
        self.set_description(data.get('description', None))
        self.parent = (data.get('parent', None), None)
        self.work_items = {}
        self.children = {}

        self.tags = {}
        for tagref in data.get('tags', []):
            self.tags[tagref] = None

    def is_toplevel(self):
        return self.parent == (None, None)

    def set_description(self, text):
        self.description = text
        if self.description:
            self.description = self._resolve_uml(self.description)
            self.description = md.convert(self.description)

    def _resolve_uml(self, text):
        inside_uml = False
        uml_content = []
        resolved_text = []
        for line in text.splitlines():
            if inside_uml:
                if line.strip() == '@enduml':
                    url = self._generate_uml_image(uml_content)
                    resolved_text.append(url)
                    inside_uml = False
                else:
                    uml_content.append(line.strip())
            else:
                if line.strip() == '@startuml':
                    uml_content = []
                    inside_uml = True
                else:
                    resolved_text.append(line)
        return '\n'.join(resolved_text)

    def _generate_uml_image(self, uml):
        url = '/plantuml/%s' % base64.urlsafe_b64encode(
            zlib.compress("\n".join(uml)))
        return '[![UML diagram](%s)](%s)' % (url, url)

    def get_parents(self):
        parents = []
        if hasattr(self, 'parent'):
            if self.parent[1]:
                parents.append(self.parent)
        if hasattr(self, 'parents'):
            for path, parent in self.parents.iteritems():
                if parent:
                    parents.append((path, parent))
        return parents

    def get_children(self):
        raise NotImplementedError

    def inherited_requirements(self, **kwargs):
        results = set()
        queue = collections.deque()
        queue.extend(self.get_parents())
        while queue:
            path, element = queue.popleft()
            if hasattr(element, 'mapped_here'):
                for ref, req in element.mapped_here.iteritems():
                    results.add((ref, req))
            queue.extend(element.get_parents())
        return mustard.sorting.sort_elements(results, kwargs)

    def mapped_requirements(self, **kwargs):
        results = set()
        for ref, req in self.mapped_here.iteritems():
            results.add((ref, req))
        return mustard.sorting.sort_elements(results, kwargs)

    def delegated_requirements(self, **kwargs):
        results = set()
        queue = collections.deque()
        queue.extend(self.get_children())
        while queue:
            path, element = queue.popleft()
            if hasattr(element, 'mapped_here'):
                for ref, req in element.mapped_here.iteritems():
                    results.add((ref, req))
            queue.extend(element.get_children())
        return mustard.sorting.sort_elements(results, kwargs)


class ElementFactory(object):

    def create(self, data):
        data['kind'] = kind_aliases.get(data['kind'], data['kind'])
        if data['kind'] == 'requirement':
            return mustard.requirement.Requirement(data)
        elif data['kind'] == 'tag':
            return mustard.tag.Tag(data)
        elif data['kind'] == 'component':
            return mustard.component.Component(data)
        elif data['kind'] == 'work-item':
            return mustard.workitem.WorkItem(data)
        elif data['kind'] == 'interface':
            return mustard.interface.Interface(data)
        elif data['kind'] == 'integration-strategy':
            return mustard.integration.IntegrationStrategy(data)
        elif data['kind'] == 'verification-criterion':
            return mustard.criterion.VerificationCriterion(data)
        elif data['kind'] == 'project':
            return mustard.project.Project(data)
        else:
            raise cliapp.AppException('Unknown element: %s' % data)
