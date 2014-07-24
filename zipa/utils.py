from copy import deepcopy


def dict_merge(first, second):
    '''Recursively merges dicts.

    Not just simply first['key'] = second['key'].
    If both first and second have a key who's value is a dict then dict_merge
    is called on both values and the result is stored in the returned
    dictionary.
    '''

    if not isinstance(second, dict):
        return second

    result = deepcopy(first)
    for key, value in second.iteritems():
        if key in result and isinstance(result[key], dict):
                result[key] = dict_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result
