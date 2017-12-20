def liquify(*args):
    liquified = list()
    for solid in args:
        current = dict()
        if not hasattr(solid, "__liquify__"):  # we cannot liquify
            current[solid.__class__.__name__] = "unliquifiable"
            continue
        ingredients = solid.__liquify__
        for attr_name in ingredients["attributes"]:
            attribute = getattr(solid, attr_name)
            if _iscustom(attribute):
                attribute = liquify(attribute)
            current[attr_name] = attribute
        liquified.append(current)
    if len(liquified) == 1:
        return liquified[0]
    return liquified


def _iscustom(o):
    """Determines if the object passed in is a custom object"""
    return not isinstance(o, (str, int, float, bool))
