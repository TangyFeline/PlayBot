from random import choice

# =~=~=~=~=~=~=~==~ Helper Functions =~=~=~=~=~=~=~=~=~ #
def MSG(text_to_format, **kwargs):
    for kwarg_value in kwargs.values():
        if hasattr(kwarg_value, 'pick_pronouns'):
            kwarg_value.pick_pronouns()

    if isinstance(text_to_format, list):
        text_to_format = choice(text_to_format)
    return text_to_format.format(**kwargs)

def pretty_list(items):
    if len(items) <= 1:
        return ", ".join(items)
    else:
        return ", ".join(items[:-1]) + " or " + items[-1]