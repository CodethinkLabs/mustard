#!/usr/bin/env python
#
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
