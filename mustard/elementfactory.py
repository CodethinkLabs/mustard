# Copyright (C) 2012 Codethink Limited


import cliapp
import markdown

import mustard


class Element(mustard.elementtrie.Trie):

    def __init__(self, data):
        mustard.elementtrie.Trie.__init__(self)

        self.kind = data.get('kind', None)
        self.title = data.get('title', None)
        self.description = data.get('description', None)
        if self.description:
            self.description = markdown.markdown(self.description)

        self.tags = {}
        for tagref in data.get('tags', []):
            self.tags[tagref] = None


class ElementFactory(object):
    
    def create(self, data):
        if data['kind'] == 'requirement':
            return mustard.requirement.Requirement(data)
        elif data['kind'] == 'tag':
            return mustard.tag.Tag(data)
        elif data['kind'] == 'architecture':
            return mustard.architecture.Architecture(data)
        elif data['kind'] == 'component':
            return mustard.component.Component(data)
        else:
            raise cliapp.AppException('Unknown element: %s' % data)
