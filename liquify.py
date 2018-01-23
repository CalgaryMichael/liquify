import re
import inspect
from collections import defaultdict


def liquify(*args):
    if len(args) == 0:
        raise ValidationError("liquify must be passed an argument")
    elif len(args) > 1:
        liquifier = liquify_multiple
    else:
        liquifier = liquify_single
    return liquifier(*args)


def liquify_single(solid):
    liquified = None
    try:
        ingredients = solid.__liquify__
    except AttributeError:
        ingredients = parse_ingredients(solid)
    if isinstance(ingredients, list):
        liquified = liquify_list(solid, ingredients)
    else:
        liquified = liquify_dict(solid, ingredients)
    return liquified


def liquify_multiple(*args):
    processed = defaultdict(list)
    for solid in args:
        group = get_liquify_group(solid)
        processed[group].append(liquify_single(solid))
    return processed


def liquify_list(solid, ingredients):
    if not isinstance(ingredients, list):
        raise TypeError("Ingredients must be a list")
    return dict(liquify_attr(solid, attr_name) for attr_name in ingredients)


def liquify_dict(solid, ingredients):
    if not isinstance(ingredients, dict):
        raise TypeError("Ingredients must be a dictionary")
    attributes = ingredients["attributes"]
    return dict(liquify_attr(solid, attr_name) for attr_name in attributes)


def liquify_attr(solid, attr_name):
    attribute = getattr(solid, attr_name)
    if inspect.ismethod(attribute):
        attribute = attribute()
    builtin = (str, int, float, bool, list, dict, tuple, set)
    if not isinstance(attribute, builtin):
        attribute = liquify(attribute)
    return attr_name, attribute


def parse_ingredients(solid):
    attributes = inspect.getmembers(solid, lambda x: not inspect.isroutine(x))
    return list(attr for attr, value in attributes if not attr.startswith("_"))


def get_liquify_group(solid):
    group = _convert(solid.__class__.__name__)
    if hasattr(solid, "__liquify__"):
        ingredients = solid.__liquify__
        if isinstance(ingredients, dict) and ingredients.get("group"):
            group = solid.__liquify__["group"]
    return group


_camel_case_converter = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
def _convert(name):
    return _camel_case_converter.sub(r'_\1', name).lower()
