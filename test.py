#!/usr/bin/env python

import cliapp
import sys

import mustard


app = cliapp.Application()

repo = sys.argv[1]
ref = sys.argv[2]

repository = mustard.repository2.Repository(repo)
cache = mustard.state2.Cache(app, repository)
state = cache.get(ref)
raw_tree_cache = mustard.rawtree.Cache()
raw_tree = raw_tree_cache.get(state)

element_tree_cache = mustard.elementtree.Cache(raw_tree_cache)
element_tree = element_tree_cache.get(state)
