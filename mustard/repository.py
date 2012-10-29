# Copyright (C) 2012 Codethink Limited


import collections
import markdown
import os
import yaml


class Repository(object):
    
    def __init__(self, dirname):
        self.dirname = dirname
        self.objects = {}
        self.load()

    def load(self):
        # collect all objects from the project dir
        for root, dirs, files in os.walk(self.dirname):
            # do not recurse into hidden subdirectories
            dirs[:] = [x for x in dirs if not x.startswith('.')]

            # skip all non-YAML files
            files[:] = [x for x in files if x.endswith('.yaml')]

            # load all YAML files into the object store
            self.load_files(root, files)

        self.process_crosslinks()

    def load_files(self, dirname, files):
        for filename in [os.path.join(dirname, x) for x in files]:
            with open(filename) as f:
                path = os.path.relpath(filename, self.dirname)[0:-len('.yaml')]
                data = yaml.load(f)
                self.load_objects(filename, path, data)

    def load_objects(self, filename, path, data):
        stack = collections.deque()
        stack.append((path, data))
        while stack:
            path, element = stack.pop()

            if isinstance(element, dict):
                if 'kind' in element:
                    if path not in self.objects:
                        self.load_object(path, element)
                    else:
                        raise cliapp.AppException(
                                'Duplicate object \"%s\" found in \"%s\"' %
                                (path, filename))
                else:
                    for child_path, child in element.iteritems():
                        stack.append((child_path, child))
            else:
                raise cliapp.AppException(
                        'Invalid element \"%s\" found in file \"%s\"' %
                        (path, filename))

    def load_object(self, path, element):
        element['path'] = path
        element['description'] = markdown.markdown(element['description'])
        self.objects[path] = element

    def process_crosslinks(self):
        for path, element in self.objects.iteritems():
            self.process_tags(self, element)

    def process_tags(self, element):
        if 'tags' in element:
            for tagref in element['tags']:
                pass

    def requirements(self):
        return [x for x in self.objects.itervalues()
                if x['kind'] == 'requirement']
