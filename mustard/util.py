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


import collections

import yaml
import yaml.constructor

class OrderedDictYAMLLoader(yaml.cyaml.CLoader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.cyaml.CLoader.__init__(self, *args, **kwargs)

        self.add_constructor(
            u'tag:yaml.org,2002:map',
            type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = collections.OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None, None, 'expected a mapping node, but found %s' % node.id,
                node.start_mark)

        mapping = collections.OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    'while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' %
                    exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


class OrderedDictYAMLDumper(yaml.Dumper):

    def __init__(self, *args, **kwargs):
        yaml.Dumper.__init__(self, *args, **kwargs)

        self.add_representer(collections.OrderedDict,
                             type(self).represent_ordered_dict)

    def represent_ordered_dict(self, odict):
        return self.represent_ordered_mapping(u'tag:yaml.org,2002:map', odict)

    def represent_ordered_mapping(self, tag, omap):
        value = []
        node = yaml.MappingNode(tag, value)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        for item_key, item_value in omap.iteritems():
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, yaml.ScalarNode)
                    and not node_key.style):
                best_style = False
            if not (isinstance(node_value, yaml.ScalarNode)
                    and not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if self.default_flow_style is not None:
            node.flow_style = self.default_flow_style
        else:
            node.flow_style = best_style
        return node


def load_yaml(src, basename=''):
    '''Load YAML from the given source.

    This also annotates the mappings with a location key.
    '''
    out = yaml.load(src, Loader=OrderedDictYAMLLoader)

    def walk(element, counter):
        element['_location'] = '%s:%d' % (basename, counter)
        counter += 1
        for ele in element.values():
            if isinstance(ele, dict):
                counter = walk(ele, counter)
        return counter

    assert (isinstance(out, dict))

    walk(out, 0)

    return out
