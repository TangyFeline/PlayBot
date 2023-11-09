from random import choice

# =~=~=~=~=~=~=~==~ Helper Functions =~=~=~=~=~=~=~=~=~ #
def MSG(text_to_format, **kwargs):
    for kwarg_value in kwargs.values():
        if hasattr(kwarg_value, 'pick_pronouns'):
            kwarg_value.pick_pronouns()

    if isinstance(text_to_format, list):
        text_to_format = choice(text_to_format)
    return text_to_format.format(**kwargs)

def pretty_list(items, delim=", ", andor="or"):
    if len(items) <= 1:
        return delim.join(items)
    else:
        return delim.join(items[:-1]) + f" {andor} " + items[-1]
def is_end_punctuation(char):
    return char in [".", "!", "?"]

def is_pause_punctuation(char):
    return char in [",", "-"]
     