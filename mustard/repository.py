# Copyright (C) 2012 Codethink Limited


import cliapp
import collections
import markdown
import os
import StringIO
import yaml

import mustard


class Repository(object):
    
    def __init__(self, state, settings):
        self.state = state
        self.project = mustard.project.Project()
        self.project.repository = self
        self.element_factory = mustard.elementfactory.ElementFactory()
        self.load()

    def load(self):
        # load all YAML files into the element tree
        for filename in self.state.list_tree():
            path = filename[0:-len('.yaml')]
            io = StringIO.StringIO(self.state.read(filename))
            data = yaml.load(io)
            self.load_elements(filename, path, data)

    def load_elements(self, filename, path, data):
        stack = collections.deque()
        stack.append((path, data))
        while stack:
            path, element = stack.pop()

            if isinstance(element, dict):
                if 'kind' in element:
                    if not self.project.lookup(path):
                        self.load_element(path, element)
                    else:
                        raise cliapp.AppException(
                                'Duplicate element \"%s\" found in \"%s\"' %
                                (path, filename))
                else:
                    for child_path, child in element.iteritems():
                        stack.append((os.path.join(path, child_path), child))
            else:
                raise cliapp.AppException(
                        'Invalid element \"%s\" found in file \"%s\"' %
                        (path, filename))

    def load_element(self, path, element):
        if path == 'project':
            self.project.title = element.get('title', None)
            self.project.set_description(element.get('description', None))
            self.project.copyright = element.get('copyright', None)
            self.project.predefined_filters = element.get(
                    'predefined-filters', [])
        else:
            element = self.element_factory.create(element)
            element.repository = self
            if not element.title:
                element.title = os.path.basename(path)
            self.project.insert(path, element)

    def process_tags(self, element):
        if 'tags' in element:
            for tagref in element['tags']:
                pass

    def requirements(self):
        return sorted([(x,y) for x,y in self.project.find('requirement')])

    def tags(self):
        return sorted([(x,y) for x,y in self.project.find('tag')])

    def architectures(self):
        return sorted([(x,y) for x,y in self.project.find('architecture')])

    def components(self):
        return sorted([(x,y) for x,y in self.project.find('component')])

    def work_items(self):
        return sorted([(x,y) for x,y in self.project.find('work-item')])

    def interfaces(self):
        return sorted([(x,y) for x,y in self.project.find('interface')])
