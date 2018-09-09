def asbool(obj):
    """
    Interprets an object as a boolean value.
    :rtype: bool
    """

    if isinstance(obj, str):
        obj = obj.strip().lower()
        if obj in ("true", "yes", "on", "y", "t", "1"):
            return True
        if obj in ("false", "no", "off", "n", "f", "0"):
            return False
        raise ValueError('Unable to interpret value "%s" as boolean' % obj)
    return bool(obj)
