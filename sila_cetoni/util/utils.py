def invert_dict(d: dict) -> dict:
    return dict([(v, k) for k, v in d.items()])
