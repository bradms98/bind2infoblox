class b2i():
    """ Class to represent a BIND to InfoBlox CSV object. """
    # strip trailing '.' character from a string. 
    # BIND uses trailing .'s in it's addresses, InfoBlox does not
    @staticmethod 
    def stripdot(strAddr):
        return strAddr.strip(" .")

    @staticmethod 
    def name2fqdn(fqdn,domain):
        # convert shorthand names to fqdn
        #print('Output: ' + fqdn)
        if not fqdn.endswith('.'):
            fqdn = fqdn + '.' + domain
        # strip trailing '.' from names that are already fqdn
        else:
            fqdn = b2i.stripdot(fqdn)
        #print('Output: ' + fqdn)
        return fqdn

    # get the domain name (ie: servicemaster.com) from the SOA record
    @staticmethod 
    def get_domain(string):
        words = string.split()
        try:
            recordType = words[3]
            fqdn = words[0]
        except:
            return()
        
        # return the fqdn of the SOA record only
        if recordType.upper() == "SOA":
            return(b2i.stripdot(fqdn))
        else:
            return()

    # Function to parse bind format lines. Returns lines in InfoBlox CSV format
    @staticmethod
    def bind2csv(string, domain):
        # Build variables from passed-in line
        
        # split incoming line into a list of words separated by spaces
        words = string.split()
        try:
            newstring = ''
            fqdn = words[0]
            ttl = words[1]
            txt_class = words[2]
            recordType = words[3]
            index = ''
            target = ''
            text = ''
            priority = ''
            weight = ''
            port = ''
        except Exception as e:
            # Return a space for empty lines. We'll cull those before writing output
            return(' ')

        # convert shorthand names to fqdn
        if not fqdn.endswith('.'):
            fqdn = fqdn + '.' + domain
        # strip trailing '.' from names that are already fqdn
        else:
            fqdn = b2i.stripdot(fqdn)

        # A records
        if recordType.upper() == "A":
            target = b2i.stripdot(words[4])
            newstring = 'arecord' + ',' + target + ',,' + fqdn + ',,,FALSE,STATIC,,FALSE,FALSE,' + ttl + ',External'
        
        # CNAME records
        if recordType.upper() == "CNAME":
            target = b2i.stripdot(words[4])
            newstring = 'cnamerecord' + ',' + fqdn + ',,' + target + ',,STATIC,,FALSE,FALSE,' + ttl + ',External,,,,,,,,,,,,,'

        # MX records
        if recordType.upper() == "MX":
            priority = words[4]
            target = b2i.stripdot(words[5])
            newstring = 'mxrecord' + ',' + fqdn + ',,' + target + ',,' + priority + ',,,STATIC,,FALSE,FALSE,' + ttl + ',External,,,,,,,,,,'

        # SRV Records
        if recordType.upper() == "SRV":
            priority = words[4]
            weight = words[5]
            port = words[6]
            target = b2i.stripdot(words[7])
            newstring = 'srvrecord' + ',' + fqdn + ',,' + port + ',,' + priority + ',,' + target + ',,' + weight + ',,,STATIC,,FALSE,FALSE,' + ttl + ',External,,,,,,'

        # TXT records
        if recordType.upper() == "TXT":
            length = len(words)
            i = 4
            while i < length:
                text = text + words[i] + ' '
                i += 1
            #strip trailing space
            text = text[:-1]
            # convert double-quotes to triple-double-quotes, as needed by InfoBlox
            text = text.replace('"','"""',)
            newstring = 'txtrecord' + ',' + fqdn + ',,' + text + ',,,STATIC,,FALSE,FALSE,' + ttl + ',External,,,,,,,,,,,,'
        
        # TODO: Handle any other record types not handled above
        # Right now, nothing else is required 
        # Purposely omitting SOA, and NS records as they must be recreated
        # Purposely omitting hostrecord and hostaddress as these are InfoBlox constructs, not used in BIND9

        #return new line in correct format
        return(newstring + '\n')




    def __init__(self, bindInput):
        self.bindInput = bindInput
        self.domain = ''
        #self.csvOutput = b2i.bind2csv(bindInput)
        output = list()
        temp = list()

        # setup headers
        output.append('header-arecord,address*,_new_address,fqdn*,_new_fqdn,comment,create_ptr,creator,ddns_principal,ddns_protected,disabled,ttl,view\n')
        output.append('header-cnamerecord,fqdn*,_new_fqdn,canonical_name,comment,creator,ddns_principal,ddns_protected,disabled,ttl,view,EA-Site,,,,,,,,,,,,\n')
        output.append('header-hostaddress,address*,_new_address,parent*,boot_file,boot_server,broadcast_address,configure_for_dhcp,configure_for_dns,deny_bootp,domain_name,domain_name_servers,ignore_dhcp_param_request_list,lease_time,mac_address,match_option,network_view,next_server,option_logic_filters,pxe_lease_time,pxe_lease_time_enabled,routers,use_for_ea_inheritance,view\n')
        output.append('header-hostrecord,fqdn*,_new_fqdn,addresses,aliases,cli_credentials,comment,configure_for_dns,_new_configure_for_dns,created_timestamp,creator_member,ddns_protected,disabled,enable_discovery,enable_immediate_discovery,ipv6_addresses,network_view,override_cli_credentials,override_credential,snmpv1v2_credential,snmpv3_credential,ttl,use_snmpv3_credential,view\n')
        output.append('header-mxrecord,fqdn*,_new_fqdn,mx*,_new_mx,priority*,_new_priority,comment,creator,ddns_principal,ddns_protected,disabled,ttl,view,,,,,,,,,,\n')
        output.append('header-srvrecord,fqdn*,_new_fqdn,port*,_new_port,priority*,_new_priority,target*,_new_target,weight*,_new_weight,comment,creator,ddns_principal,ddns_protected,disabled,ttl,view,,,,,,\n')
        output.append('header-txtrecord,fqdn*,_new_fqdn,text*,_new_text,comment,creator,ddns_principal,ddns_protected,disabled,ttl,view,,,,,,,,,,,,\n')

        for s in bindInput.splitlines():
            temp.append(s.strip())        

        # determine the domain name we're working with
        for line in temp:
            result = b2i.get_domain(line)
            if len(result) != 0:
                self.domain = result
                break

        # Read inFile and convert it according to bind2csv
        for line in temp:
            # convert to InfoBlox' format
            newline = b2i.bind2csv(line, self.domain)
            # don't append empty lines
            if not newline.isspace():
                output.append(newline.rstrip() + '\n')		

        # Write output
        self.csvOutput = output