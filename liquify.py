import inspect


def liquify(*args):
    processed = list()
    for solid in args:
        try:
            ingredients = solid.__liquify__
        except AttributeError:
            raise AttributeError("unliquifiable")
        if isinstance(ingredients, list):
            processed.append(liquify_list(solid, ingredients))
        else:
            processed.append(liquify_dict(solid, ingredients))
    if len(processed) == 1:
        return processed[0]
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
    if not isinstance(attribute, (str, int, float, bool, list, dict, tuple)):
        attribute = liquify(attribute)
    return attr_name, attribute


def append(dictionary, key, value):
    current_value = dictionary.get(key)
    if not current_value:
        dictionary[key] = [value]
    else:
        if not isinstance(current_value, list):
            raise AttributeError("Cannot append to a non-list item")
        else:
            current_value.append(value)
