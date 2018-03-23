import re
import inspect
from collections import defaultdict, namedtuple

MAX_DEPTH = 10

DEFAULT_DEPTH = 2

BUILT_IN = (str, int, float, bool, list, dict, tuple, set)

_camel_case_converter = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

LiquifyRule = namedtuple("LiquifyRule", ["name", "rule"])


def liquify(*args, **kwargs):
    if len(args) == 0:
        raise ValidationError("liquify must be passed an argument")
    elif len(args) > 1:
        liquifier = liquify_multiple
    else:
        liquifier = liquify_single
    depth = min(kwargs.pop("depth", DEFAULT_DEPTH), MAX_DEPTH)
    ingredients = kwargs.get("ingredients")
    if ingredients is not None:
        # assert that all classes are the same
        if not all(isinstance(arg, type(args[0])) for arg in args):
            raise TypeError("Cannot liquify multiple classes with explicit ingredients")
    return liquifier(*args, ingredients=ingredients, depth=depth)


def liquify_single(solid, ingredients=None, depth=DEFAULT_DEPTH):
    liquified = None
    if ingredients is None:
        ingredients = parse_ingredients(solid)
    try:
        ingredients = ingredients["attributes"]
    except TypeError:
        pass
    return dict(liquify_ingredient(solid, ingredient, depth) for ingredient in ingredients)


def liquify_multiple(*args, **kwargs):
    processed = defaultdict(list)
    for solid in args:
        group = get_liquify_group(solid)
        processed[group].append(liquify_single(solid, **kwargs))
    return processed


def liquify_ingredient(solid, ingredient, depth=DEFAULT_DEPTH):
    if isinstance(ingredient, LiquifyRule):
        attr_name = ingredient.name
        attribute = ingredient.rule(solid)
    else:
        attr_name = ingredient
        attribute = getattr(solid, attr_name)
        if inspect.ismethod(attribute):
            attribute = attribute()
        if not isinstance(attribute, BUILT_IN):
            if depth > 0:
                attribute = liquify(attribute, depth=depth - 1)
            else:
                attribute = str(attribute)
    return attr_name, attribute


def parse_ingredients(solid):
    try:
        return solid.__liquify__
    except AttributeError:
        attributes = inspect.getmembers(solid, lambda x: not inspect.isroutine(x))
        return list(attr for attr, value in attributes if not attr.startswith("_"))


def get_liquify_group(solid):
    group = _convert(solid.__class__.__name__)
    if hasattr(solid, "__liquify__"):
        ingredients = solid.__liquify__
        if isinstance(ingredients, dict) and ingredients.get("group"):
            group = solid.__liquify__["group"]
    return group


def _convert(name):
    return _camel_case_converter.sub(r'_\1', name).lower()
