class Domain:
    """
    A Domain represents a domain usable by the DNS system.
    """

    def __init__(self, name = 'example.com'):
        """
        Describe the method
        """
        self.name = name

    def __repr__(self):
        return self.name