from zope import schema

class InvalidStandardNumber(schema.ValidationError):
    "Number does not conform to the standard."
    
def stdnum_validator(type):
    """ factory for simple stdnum based validators """

    def validator(value):
        stdmod = getattr(__import__('stdnum', fromlist=[type]), type)
        try:
            if not stdmod.is_valid(value):
                raise
        except:
            raise InvalidStandardNumber(value)
        return True
    
    return validator
