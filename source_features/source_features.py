from ipstack import GeoLookup
import subprocess

from AutonomousSystemFeatures.AutonomousSystemFeaturesExtractor import AutonomousSystemFeaturesExtractor
from IpStackFeatures.IpStackFeaturesExtractor import IpStackFeaturesExtractor
from NetworkFeatures.NetworkFeaturesExtractor import NetworkFeaturesExtractor

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



