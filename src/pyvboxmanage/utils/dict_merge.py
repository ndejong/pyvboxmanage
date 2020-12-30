
def dict_merge(a, b, path=None):
    if path is None:
        path = []
    for key in b.keys():
        if key in a.keys() and isinstance(a[key], dict) and isinstance(b[key], dict):
            dict_merge(a[key], b[key], path + [str(key)])
        else:
            a[key] = b[key]
    return a
