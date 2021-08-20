import subprocess
#https://github.com/john-kurkowski/tldextract
import tldextract

class NetworkFeaturesExtractor():
    def get_tracepath_query(self,url):
        tracepath_query  = subprocess.run(["tracepath", "-b", url], capture_output=True, text=True)
        return tracepath_query

    def get_dig_query(self,url, entryType):
        dig_query = subprocess.run(["dig" , url, entryType], capture_output=True, text=True)
        return dig_query

    def get_main_domain_from_url(self,url):
        dissectedUrl = tldextract.extract(url)
        main_domain = dissectedUrl.domain+"."+dissectedUrl.suffix
        #print("Main domain usado para o network feaures", main_domain , "\n")
        return main_domain

        # domain = url.split("://")[1].split("/")[0]
        # domain = domain.replace("www.", "")
        # print("Domain usado para o network feaures", domain , "\n")
        # return domain

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

    def get_network_data(self,url):
        domain = self.get_main_domain_from_url(url)
        network_data = dict()

        tracepath_query = self.get_tracepath_query(domain)
        network_data['domain_route_hops'] = self.get_route_hop_count(tracepath_query)

        caa_query = self.get_dig_query(domain, "CAA")
        txt_query = self.get_dig_query(domain, "TXT")
        network_data['domain_dns_caa_txt_count'] = self.get_dns_CAA_TXT_entry_count(caa_query,txt_query)

        return network_data
