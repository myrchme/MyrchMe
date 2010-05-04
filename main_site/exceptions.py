"""
exceptions.py
Holds our project's custom exceptions.
"""
class NoMerchForPerson(Exception):
    """
    NoMerchForPerson:
    Raised if there are no products that fit a given users preferences.
    """
    def __init__(self, value):
       self.parameter = value
    def __str__(self):
       return repr(self.parameter)


class NoMerchAtAll(Exception):
    """
    NoMerchAvailable:
    Raised if there are no products available.
    """
    def __init__(self, value):
       self.parameter = value
    def __str__(self):
       return repr(self.parameter)

