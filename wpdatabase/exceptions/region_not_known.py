""" Raised when the Amazon Web Services (AWS) region is not known. """


class RegionNotKnownError(Exception):
    """ Raised when the Amazon Web Services (AWS) region is not known. """

    def __init__(self):
        msg = ('The Amazon Web Services (AWS) region was not set and could '
               'not be determined.')
        super().__init__(msg)
