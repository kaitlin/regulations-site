# vim: set encoding=utf-8
import itertools

from regulations.generator import generator
from regulations.generator.layers.meta import MetaLayer
from regulations.generator.layers.tree_builder import roman_nums
from regulations.generator.toc import fetch_toc


def to_roman(number):
    """ Convert an integer to a roman numeral """
    romans = list(itertools.islice(roman_nums(), 0, number + 1))
    return romans[number - 1]


def get_layer_list(names):
    layer_names = generator.LayerCreator.LAYERS
    return set(l.lower() for l in names.split(',') if l.lower() in layer_names)


def regulation_meta(regulation_part, version, sectional=False):
    """ Return the contents of the meta layer, without using a tree. """

    layer_manager = generator.LayerCreator()
    layer_manager.add_layers(['meta'], 'cfr', regulation_part, sectional,
                             version)

    p_applier = layer_manager.appliers['paragraph']
    meta_layer = p_applier.layers[MetaLayer.shorthand]
    applied_layer = meta_layer.apply_layer(regulation_part)

    return applied_layer[1]


def layer_names(request):
    """Determine which layers are currently active by looking at the request"""
    if 'layers' in request.GET.keys():
        return get_layer_list(request.GET['layers'])
    else:
        return generator.LayerCreator.LAYERS.keys()


def first_section(reg_part, version):
    """ Use the table of contents for a regulation, to get the label of the
    first section of the regulation. In most regulations, this is -1, but in
    some it's -101. """

    toc = fetch_toc(reg_part, version, flatten=True)
    return toc[0]['section_id']


def make_sortable(string):
    """Split a string into components, converting digits into ints so sorting
    works as we would expect"""
    if not string:      # base case
        return tuple()
    elif string[0].isdigit():
        prefix = "".join(itertools.takewhile(lambda c: c.isdigit(), string))
        return (int(prefix),) + make_sortable(string[len(prefix):])
    else:
        prefix = "".join(itertools.takewhile(lambda c: not c.isdigit(),
                                             string))
        return (prefix,) + make_sortable(string[len(prefix):])
