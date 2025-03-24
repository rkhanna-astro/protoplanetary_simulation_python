import numpy as np

def parse_args(args, arg_struct, flagtype_params=None, aliases=None):
    if flagtype_params is None:
        flagtype_params = []
    if aliases is None:
        aliases = []

    # Get numeric arguments
    num_arg_count = 0
    while num_arg_count < len(args) and not isinstance(args[num_arg_count], str):
        num_arg_count += 1

    arg_struct['NumericArguments'] = args[:num_arg_count] if num_arg_count > 0 else []

    # Make an accepted fieldname matrix (case insensitive)
    fnames = {k.lower(): k for k in arg_struct.keys()}
    fnames_abbr = {k.lower(): ''.join([c for c in k if c.isupper()]).lower() for k in arg_struct.keys()}
    flagtype_params = [param.lower() for param in flagtype_params]

    if aliases:
        for alias, fields in aliases:
            alias = alias.lower()
            for field in fields:
                fnames[alias] = field
                fnames_abbr[alias] = ''.join([c for c in alias if c.isupper()]).lower()

    # Get parameters
    l = num_arg_count
    while l < len(args):
        a = args[l]
        if isinstance(a, str):
            a = a.lower()
            field_idx = fnames_abbr.get(a, fnames.get(a))
            if not field_idx:
                raise ValueError(f"Unknown named parameter: {a}")

            if field_idx in flagtype_params:
                val = 1
            else:
                val = args[l + 1]
                l += 1

            arg_struct[field_idx] = val
            l += 1
        else:
            raise ValueError(f"Expected a named parameter: {a}")

    return arg_struct

# Example usage
def parseargtest(*args):
    arg_struct = {
        'Holdaxis': 0,
        'SpacingVertical': 0.05,
        'SpacingHorizontal': 0.05,
        'PaddingLeft': 0,
        'PaddingRight': 0,
        'PaddingTop': 0,
        'PaddingBottom': 0,
        'MarginLeft': 0.1,
        'MarginRight': 0.1,
        'MarginTop': 0.1,
        'MarginBottom': 0.1,
        'rows': [],
        'cols': []
    }

    arg_struct = parse_args(args, arg_struct, 
                            flagtype_params=['Holdaxis'], 
                            aliases=[('Spacing', ['SpacingHorizontal', 'SpacingVertical']), 
                                     ('Padding', ['PaddingLeft', 'PaddingRight', 'PaddingTop', 'PaddingBottom']), 
                                     ('Margin', ['MarginLeft', 'MarginRight', 'MarginTop', 'MarginBottom'])])
    print(arg_struct)

# Test the function
parseargtest('SpacingVertical', 0.1, 'Holdaxis', 'PaddingLeft', 0.2)
# ```