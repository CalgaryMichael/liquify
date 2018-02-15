import re
import inspect
import asyncio


def liquify(*args):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asnycio.new_event_loop()
    return loop.run_until_complete(_liquify(*args))


async def _liquify(*args):
    if len(args) == 0:
        raise ValidationError("liquify must be passed an argument")
    elif len(args) > 1:
        liquifier = liquify_multiple
    else:
        liquifier = liquify_single
    return await liquifier(*args)


async def liquify_single(solid):
    liquified = None
    try:
        ingredients = solid.__liquify__
    except AttributeError:
        ingredients = parse_ingredients(solid)
    if isinstance(ingredients, list):
        liquified = await liquify_list(solid, ingredients)
    else:
        liquified = await liquify_dict(solid, ingredients)
    return liquified


async def liquify_multiple(*args):
    processed = dict()
    for solid in args:
        group = get_liquify_group(solid)
        _append(processed, group, await liquify_single(solid))
    return processed


async def liquify_list(solid, ingredients):
    if not isinstance(ingredients, list):
        raise TypeError("Ingredients must be a list")
    attributes = dict()
    for attribute in ingredients:
        attr_name, value = await liquify_attr(solid, attribute)
        attributes[attr_name] = value
    return attributes


async def liquify_dict(solid, ingredients):
    if not isinstance(ingredients, dict):
        raise TypeError("Ingredients must be a dictionary")
    attributes = dict()
    for attribute in ingredients["attributes"]:
        attr_name, value = await liquify_attr(solid, attribute)
        attributes[attr_name] = value
    return attributes


async def liquify_attr(solid, attr_name):
    attribute = getattr(solid, attr_name)
    if inspect.ismethod(attribute):
        attribute = attribute()
    builtin = (str, int, float, bool, list, dict, tuple, set)
    if not isinstance(attribute, builtin):
        attribute = await _liquify(attribute)
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


def _append(dictionary, key, value):
    current_value = dictionary.get(key)
    if not current_value:
        dictionary[key] = [value]
    else:
        if not isinstance(current_value, list):
            raise AttributeError("Cannot append to a non-list item")
        else:
            current_value.append(value)
