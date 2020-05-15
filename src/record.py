import sys

class Record:
    """
    Record is an individual entry for a host in a Zone. This is an individual DNS record.
    Record has the following attributes:
        name: Can be prepended to a domain to form a FQDN. 
            Examples: www, webmail, db

        record_type: Specifies the type of record.
            Examples: A, CNAME, MX, TXT

        data: The data that is returned when a query is made for this record. 
            Examples: 
                1.2.3.4 - for A records
                webmail.example.com - for CNAME records
                "v=spf1 include:spf.protection.outlook.com -all" - for TXT records

        ttl: Time To Live. Specifies how long a querying host should cache the response
            Example: 3600

        record_class: Always 'IN' for Internet records. Other values are defined but obsolete

    Please reference:
    https://help.dyn.com/how-to-format-a-zone-file/
    https://tools.ietf.org/html/rfc1035
    """

    _supported_types = ['A', 'CNAME', 'MX', 'SOA', 'SRV', 'TXT']

    def __init__(self, name, record_type, data, ttl=3600, record_class='IN'):
        """
        Describe the method
        """
        self._errors = []
        self._supported_types = ['A', 'CNAME', 'MX', 'SOA', 'SRV', 'TXT']
        try:
            self.set_name(name)
            self.data = data
            self.ttl = ttl
            self.record_class = record_class
            self.set_type(record_type)
        except AssertionError as e: 
            e.args += (f"name={name}", f"record_type={record_type}", f"data={data}", f"ttl={ttl}", f"record_class={record_class}")
            raise

    def bind_format(self):
        """
        Returns a string formatted as you would see in a zone file for a BIND style DNS server
        """
        return (f"{self.name}\t{self.ttl}\t{self.record_class}\t{self.record_type}\t{self.data}")

    def infoblox_format(self):
        """
        Returns a string formatted as needed by an Infoblox CSV import file.
        """
        pass

    def set_name(self, name):
        assert(len(name) > 0), (f"Name cannot be empty")
        self.name = name.lower()

    def set_type(self, record_type):
        assert(record_type.upper() in self._supported_types), (f"Record Type '{record_type.upper()}' is not supported")
        self.record_type = record_type.upper()

    def __repr__(self):
        """
        Return information about a Record object in a format like BIND would use
        """
        return self.bind_format()
