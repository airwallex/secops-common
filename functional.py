""" Common functional utilities """


def merge(x, y):
    """ Merge two dicts """
    return dict(x, **y)


def compose2(f, g):
    """Compose 2 functions"""
    return lambda *a, **kw: f(g(*a, **kw))


def flatten(items):
    return [item for sublist in items for item in sublist]


def dict_sum(dicts):
    output = {}
    for d in dicts:
        for key, value in d.items():
            if key in output:
                output[key] += value
            else:
                output[key] = value
    return output
