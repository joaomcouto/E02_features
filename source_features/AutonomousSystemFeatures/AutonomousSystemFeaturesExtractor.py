import subprocess

class AutonomousSystemFeaturesExtractor():

    def get_ASN_query(self,ip_addr):
        whois_query  = subprocess.run(["whois" , "-h", "whois.cymru.com", "-v" ,ip_addr], capture_output=True, text=True)
        return whois_query

    #"186.192.81.5"
    def get_col_data(self,colName, whois_query):
        for i,line in enumerate(whois_query.stdout.splitlines()):
            if ("AS" in line and "IP" in line):
                query_header = line.split("|")
                for j,col in enumerate(query_header):
                    if (colName in col):
                        break
                return whois_query.stdout.splitlines()[i+1].split("|")[j].strip()


    def get_as_n(self,whois_query):
        return self.get_col_data("AS", whois_query)

    def get_as_cc(self,whois_query):
        return self.get_col_data("CC", whois_query)

    def get_asn_data(self,ip_addr):
        asn_data = dict()
        whois_query = self.get_ASN_query(ip_addr)

        asn_data['as_n'] = self.get_as_n(whois_query)
        asn_data['as_cc'] = self.get_as_cc(whois_query)

        return asn_data