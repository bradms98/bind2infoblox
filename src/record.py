import sys
import string

class Record:
    """
    Record is an individual entry for a host in a Zone. This is an individual DNS record.
    Record has the following attributes:
        name: Can be prepended to a base_domain to form a FQDN. 
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
    https://tools.ietf.org/html/rfc1035
    https://help.dyn.com/how-to-format-a-zone-file/
    """

    #private data
    _supported_types = ['A', 'CNAME', 'MX', 'NS', 'SOA', 'SRV', 'TXT']
    _errors = []

    def __init__(self, name, record_type, data, base_domain='', ttl=3600, priority=100, weight=1, port=0, record_class='IN'):
        """
        TODO: implement doctest
        """
        # Do error checking on required parameters
        try:
            self.set_name(name)
            self.set_type(record_type)
            self.set_data(data)
            self.set_base_domain(base_domain)
        except AssertionError as e: 
            e.args += (f"name={name}", f"record_type={record_type}", f"data={data}", f"ttl={ttl}", f"record_class={record_class}")
            raise

        self.ttl = ttl
        self.priority = priority
        self.weight = weight
        self.port = port
        self.record_class = record_class
        
    def bind_format(self):
        """
        Returns a string formatted as you would see in a zone file for a BIND style DNS server
        """
        if self.record_type == 'MX':
            return (f"{self.name}\t{self.ttl}\t{self.record_class}\t{self.record_type}\t{self.priority}\t{self.data}")
        elif self.record_type == 'SVR':
            return (f"{self.name}\t{self.ttl}\t{self.record_class}\t{self.record_type}\t{self.priority}\t{self.weight}\t{self.port}\t{self.data}")
        else:   # Any other record_type (A, CNAME, NS, SOA, TXT)
            return (f"{self.name}\t{self.ttl}\t{self.record_class}\t{self.record_type}\t{self.data}")

    def infoblox_format(self, base_domain=''):
        """
        Returns a string formatted as needed by an Infoblox CSV import file.
        """
        if len(base_domain) > 0:
            self.set_base_domain(base_domain)

        assert(len(self.base_domain) > 0), (f"base_domain is required when using infoblox format")
        # A records
        if self.record_type == "A":
            return (f"arecord,{self.data},,{self.fqdn},,,FALSE,STATIC,,FALSE,FALSE,{self.ttl},External")
        elif self.record_type == "CNAME":
            return (f"cnamerecord,{self.fqdn},,{self.data},,STATIC,,FALSE,FALSE,{self.ttl},External,,,,,,,,,,,,,")
        elif self.record_type == "MX":
            return (f"mxrecord,{self.fqdn},,{self.data},,{self.priority},,,STATIC,,FALSE,FALSE,{self.ttl},External,,,,,,,,,,")
        elif self.record_type == "SRV":
            return (f"srvrecord,{self.fqdn},,{self.port},,{self.priority},,{self.data},,{self.weight},,,STATIC,,FALSE,FALSE,{self.ttl},External,,,,,,")
        elif self.record_type == "TXT":
            return (f"txtrecord,{self.fqdn},,{self.data},,,STATIC,,FALSE,FALSE,{self.ttl},External,,,,,,,,,,,,")

    def set_name(self, name):
        assert(len(name) > 0), (f"Record name cannot be empty")
        self.name = name.strip().strip('.').lower()

    def set_type(self, record_type):
        assert(record_type.upper() in self._supported_types), (f"Record Type '{record_type.upper()}' is not supported")
        self.record_type = record_type.strip().upper()

    def set_data(self, data):
        assert(len(data) > 0), (f"Record data cannot be empty")
        self.data = data.strip()

    def set_base_domain(self, base_domain):
        self.base_domain = base_domain.strip().strip('.').lower()
        self.fqdn = f"{self.name}.{self.base_domain}"

    def __repr__(self, format='bind'):
        """
        Return information about a Record object in a format like BIND would use
        """
        if format.lower() == 'infoblox':
            return self.infoblox_format()
        else:
            return self.bind_format()
        
