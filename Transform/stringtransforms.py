class StringTransformation:
    def __init__(self, name):
        self.name = name

class CensorTransformation(StringTransformation):
    def __init__(self, *args, **kwargs):
        super().__init__("CENSOR", *args, **kwargs)

class ReplaceTransformation(StringTransformation):
    def __init__(self, *args, **kwargs):
        super().__init__("REPLACE", *args, **kwargs)


STRING_TRANSFORMS = [
    CensorTransformation(),
    ReplaceTransformation(),
]
STRING_TRANSFORMS_KEYS = [ transform.name for transform in STRING_TRANSFORMS]