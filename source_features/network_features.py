from ipstack import GeoLookup
import subprocess

class IpStackFeaturesExtractor():

    def __init__(self,ipstack_apiKey):
        self.ipstack_apiKey = ipstack_apiKey

    def get_ipstack_location_dict(self, url):
        return GeoLookup(self.ipstack_apiKey).find_hostname().get_location(url)

    def get_ip(self,ipstack_location_dict):
        return ipstack_location_dict['ip']

    def get_latitude(self,ipstack_location_dict):
        return ipstack_location_dict['latitude']

    def get_longitude(self,ipstack_location_dict):
        return ipstack_location_dict['longitude']

    def get_www_subdomain_from_url(self,url):
        domain = url.split("://")[1].split("/")[0]
        if ("www." in domain):
            pass
        else:
            domain = "www." + domain
        return domain

    def get_is_brazil(self,ipstack_location_dict):
        return ipstack_location_dict['country_name'] in ["Brazil", "brazil"]

    def get_is_us(self,ipstack_location_dict):
        return ipstack_location_dict['country_name'] in ["United States", "united states"]

    def get_country_code(self,ipstack_location_dict):
        return ipstack_location_dict['country_code']

    def get_ipstack_data(self, url):
        url = self.get_www_subdomain_from_url(url)
        ipstack_location_dict = self.get_ipstack_location_dict(url)
        #print(ipstack_location_dict)
        ipstack_data = dict()
        ipstack_data['ip'] = self.get_ip(ipstack_location_dict)
        ipstack_data['ip_cc'] = self.get_country_code(ipstack_location_dict)
        ipstack_data['ip_is_brazil'] = self.get_is_brazil(ipstack_location_dict)
        ipstack_data['ip_is_us'] = self.get_is_us(ipstack_location_dict)

        ipstack_data['ip_latitude'] = round(self.get_latitude(ipstack_location_dict),2)
        ipstack_data['ip_longitude'] = round(self.get_longitude(ipstack_location_dict),2)
        return ipstack_data

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

class NetworkFeaturesExtractor():
    def get_tracepath_query(self,url):
        tracepath_query  = subprocess.run(["tracepath", "-b", url], capture_output=True, text=True)
        return tracepath_query

    def get_dig_query(self,url, entryType):
        dig_query = subprocess.run(["dig" , url, entryType], capture_output=True, text=True)
        return dig_query

    def get_domain_from_url(self,url):
        domain = url.split("://")[1].split("/")[0]
        domain.replace("www.", "")
        return domain

    def get_route_hop_count(self,tracepath_query):
        noReplyCount = 0
        hopCount = 0
        for i,line in enumerate(tracepath_query.stdout.splitlines()):
            #print(line)
            if("no reply" in line):
                noReplyCount += 1
            else:
                hopCount = hopCount + noReplyCount + 1
                noReplyCount = 0

            if(noReplyCount >= 5):
                break
        return hopCount

    def get_dns_entry_count(self,dig_query, entryType):
        if("ANSWER SECTION" in dig_query.stdout):
            answer_section = dig_query.stdout.split(";; ANSWER SECTION:")[1].split("\n;;")[0]
        else:
            return 0
        #print(answer_section)
        #print("\n")
        entryCount = 0
        for line in answer_section.splitlines():
            #print(line)
            if("\t" + entryType + "\t" in line):
                entryCount+= 1
        return entryCount
            
    def get_dns_CAA_TXT_entry_count(self, caa_dig_query, txt_dig_query):
        caa_count = self.get_dns_entry_count(caa_dig_query, "CAA")
        txt_count = self.get_dns_entry_count(txt_dig_query, "TXT")
        return caa_count+txt_count



class SourceFeaturesExtractor(AutonomousSystemFeaturesExtractor, IpStackFeaturesExtractor, NetworkFeaturesExtractor):
    def __init__(self,ipstack_apiKey):
        super(SourceFeaturesExtractor, self).__init__(ipstack_apiKey)

    def get_ipcc_equal_ascc(self,data_asn, data_ipstack):
        return data_asn['as_cc'] == data_ipstack['ip_cc']

    def get_ip_vs_asn_data(self,data_asn, data_ipstack):
        ip_vs_asn_data = dict()
        ip_vs_asn_data['ipcc_equal_ascc'] = self.get_ipcc_equal_ascc(data_asn, data_ipstack)

        return ip_vs_asn_data


url = "https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19"
print(url + "\n")

teste = SourceFeaturesExtractor("8c4b00a0873a12e53b7a2384ad8eeb9f")

data_ipstack = teste.get_ipstack_data(url)
print(data_ipstack)
print("\n")

data_asn = teste.get_asn_data(data_ipstack['ip'])
print(data_asn)
print("\n")

data_meta = teste.get_ip_vs_asn_data(data_asn, data_ipstack)
print(data_meta)
print("\n")

data_network = teste.get_network_data(url)
print(data_network)
print("\n")



