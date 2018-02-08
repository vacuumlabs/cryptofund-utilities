def memo(f, *args):
    cache = {}
    def memoized_f(*args):
        if args not in cache: cache[args] = f(*args)
        return cache[args]
    return memoized_f
