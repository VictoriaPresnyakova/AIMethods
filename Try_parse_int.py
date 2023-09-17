def try_parse_int(string: str, default: int) -> int:
    '''helper to parse int from string without erroring on empty or misformed string'''
    try:
        return int(string)
    except Exception:
        return default
