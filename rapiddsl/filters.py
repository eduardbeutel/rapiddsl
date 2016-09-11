import re

def register_filters(env):
    env.filters['first_upper'] = first_upper
    env.filters['first_lower'] = first_lower
    env.filters['const_case'] = const_case

def const_case(x):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', x)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

def first_lower(x):
    return x[0].lower() + x[1:]

def first_upper(x):
    return x[0].upper() + x[1:]

