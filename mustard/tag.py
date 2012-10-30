# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class Tag(mustard.elementtrie.Trie):

    def __init__(self, data):
        mustard.elementtrie.Trie.__init__(self)
        
        self.description = markdown.markdown(data.get('description', ''))
