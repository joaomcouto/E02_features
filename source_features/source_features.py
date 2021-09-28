from ipstack import GeoLookup
import subprocess
# https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x

if __name__ == "__main__":
    from AutonomousSystemFeatures.AutonomousSystemFeaturesExtractor import AutonomousSystemFeaturesExtractor
    from IpStackFeatures.IpStackFeaturesExtractor import IpStackFeaturesExtractor
    from NetworkFeatures.NetworkFeaturesExtractor import NetworkFeaturesExtractor
else:
    from .AutonomousSystemFeatures.AutonomousSystemFeaturesExtractor import AutonomousSystemFeaturesExtractor
    from .IpStackFeatures.IpStackFeaturesExtractor import IpStackFeaturesExtractor
    from .NetworkFeatures.NetworkFeaturesExtractor import NetworkFeaturesExtractor
    from .RankingFeatures.RankingFeaturesExtractor import RankingFeaturesExtractor
    from .RegistryFeatures.RegistryFeaturesExtractor import RegistryFeaturesExtractor

class SourceFeaturesExtractor(AutonomousSystemFeaturesExtractor, 
                              IpStackFeaturesExtractor, 
                              NetworkFeaturesExtractor,
                              RankingFeaturesExtractor,
                              RegistryFeaturesExtractor
                             ):
    def __init__(self,ipstack_apiKey):
        IpStackFeaturesExtractor.__init__(self,ipstack_apiKey)
        RankingFeaturesExtractor.__init__(self, 0)

    def get_ipcc_equal_ascc(self,data_asn, data_ipstack):
        return data_asn['subdomain_as_cc'] == data_ipstack['subdomain_ip_cc']

    def get_ip_vs_asn_data(self,data_asn, data_ipstack):
        ip_vs_asn_data = dict()
        ip_vs_asn_data['subdomain_ipcc_equal_ascc'] = self.get_ipcc_equal_ascc(data_asn, data_ipstack)

        return ip_vs_asn_data

if __name__ == "__main__":
    url = "https://www.tercalivre.com.br/oms-recua-e-diz-que-governos-devem-pensar-em-quem-precisa-garantir-o-pao-de-cada-dia/"
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


