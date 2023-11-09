from random import choice

class CensorType:
    def __init__(self,char):
        self.char = char
        pass

    def replace(self, text):
        return len(text) * self.char    

class ErrorCensorType(CensorType):
    def __init__(self):
        pass
    
    def replace(self, text):
        print(text)
        ERRORS = [
            "ERROR",
            "NOT FOUND",
            "EXCEPTION",
            "MEMORY ERROR",
            "ACCESS DENIED",
            "NULL POINTER"
        ]
        return f"`[{choice(ERRORS)}]`"
    
    
class TextCensorType(CensorType):
    def __init__(self, text):
        self.text = text
    
    def replace(self, text):
       return self.text

CensorTypes = {
    'Censor': CensorType('█'),
    'Blank': CensorType('\_'),
    'Error': ErrorCensorType(),
    'Squeak': TextCensorType('SQUEAK')
}

EXPLAIN_CENSOR_METHODS = f"""
    **Censor** whites out forbidden words. 
    > This word is {CensorTypes['Censor'].replace('forbidden')}

    **Blank** replaces forbidden words with spaces.
    > This word is {CensorTypes['Blank'].replace('forbidden')}

    **Error** replaces forbidden words with a technical error message.
    > This word is {CensorTypes['Error'].replace('forbidden')}

    **Squeak** replaces forbidden words with a squeak.
    > This word is {CensorTypes['Squeak'].replace('forbidden')}
"""