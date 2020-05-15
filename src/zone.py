from record import Record

class Zone:
    """
    Zone represents a DNS zone, which consists of one domain and various records.
    A Zone is used by DNS servers like BIND and Infoblox
    """

    def __init__(self):
        """
        Describe the method
        """
        self._errors = []
        self.records = []
        records = []
        records.append(('www', 'CNAME', 'example.com'))
        records.append(('webmail', 'A', '1.2.3.4'))
        records.append(('balls', 'balls', 'balls'))
        records.append(('', 'MX', 'webmail.example.com'))

        for r in records:
            try:
                self.records.append(Record(r[0], r[1], r[2]))
            except AssertionError as e:
                self._errors.append(e)
    
        for error in self._errors:
            print(f"{error}")