# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Requirement(mustard.elementtrie.Trie):

    def __init__(self, data):
        mustard.elementtrie.Trie.__init__(self)
        
        self.description = markdown.markdown(data.get('description', ''))

        self.tags = {}
        for tagref in data.get('tags', []):
            self.tags[tagref] = None
