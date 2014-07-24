from copy import deepcopy


def dict_merge(first, second):
    '''Recursively merges dict's.

    Not just simple first['key'] = second['key'], if
    both first and second have a key who's value is a dict then dict_merge is
    called on both values and the result stored in the returned dictionary.
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
