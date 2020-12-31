
def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b.keys():
        if key in a.keys() and type(a[key]) is dict and type(b[key]) is dict:
            merge(a[key], b[key], path + [str(key)])
        elif key in a.keys() and type(a[key]) is list and type(b[key]) is list:
            a[key].extend(b[key])
        else:
            a[key] = b[key]
    return a
