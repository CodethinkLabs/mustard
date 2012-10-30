# Copyright (C) 2012 Codethink Limited


import cliapp

import mustard


class Project(mustard.elementtrie.Trie):

    def __init__(self):
        mustard.elementtrie.Trie.__init__(self)

        self.requirements = {}
        self.tags = {}

    def _propagate_requirement(self, path, requirement):
        self.requirements[path] = requirement

        for tagref in requirement.tags.iterkeys():
            if tagref in self.tags:
                requirement.tags[tagref] = self.tags[tagref]
            else:
                raise cliapp.AppException(
                    'Tag \"%s\" used by \"%s\" not found' % (tagref, path))

    def _propagate_tag(self, path, tag):
        self.tags[path] = tag

        for requirements in self.requirements.itervalues():
            if path in requirements.tags:
                requirements.tags[path] = tag
