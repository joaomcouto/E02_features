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

    def get_domain_from_url(self,url):
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
        url = self.get_domain_from_url(url)
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


url = "https://www.uol.com.br/"
print(url + "\n")

ipstack_data_extractor = IpStackFeaturesExtractor("8c4b00a0873a12e53b7a2384ad8eeb9f")
data_ipstack = ipstack_data_extractor.get_ipstack_data(url)

print(data_ipstack)
print("\n")

