""" Raised when the region is not known. """


class RegionNotKnownError(Exception):
    """ Raised when the region is not known. """

    def __init__(self):
        msg = 'The AWS region was not set and could not be determined.'
        super().__init__(msg)
