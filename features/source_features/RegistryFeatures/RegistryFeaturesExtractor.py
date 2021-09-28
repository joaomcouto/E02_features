import subprocess
#https://github.com/john-kurkowski/tldextract
import tldextract
import numpy as np
import pandas as pd
from datetime import datetime
import time
import logging

class RegistryFeaturesExtractor():
    def get_whois_query(self,url):
        whois_query = subprocess.run(["whois" , url], capture_output=True, text=True)
        return whois_query

    def get_main_domain_from_url(self,url):
        dissectedUrl = tldextract.extract(url)
        main_domain = dissectedUrl.domain+"."+dissectedUrl.suffix
        return main_domain

    def get_whois_line_entry(self,fieldPattern, fieldLimiter, whois_query):
        if(fieldPattern in whois_query.stdout):
            entry = whois_query.stdout.split(fieldPattern)[1].split(fieldLimiter)[0].strip()
            if(len(entry)>0):
                return entry
            else:
                return -1
        else:
            return -1
        
    def attempt_entry_formats(self,formatList,whois_query):
        attemptCount = 0
        for pattern,limiter in formatList:
            attemptCount = attemptCount + 1
            #print("Trying pattern", pattern,limiter)
            res = self.get_whois_line_entry(pattern, limiter,whois_query)
            #print("Res", res)
            if(res!= -1):
                break
            if(attemptCount== len(formatList)):
                res = ""
        #print('Res antes do split ', res )
        if("#" in res):
            res = res.split(' #')[0]
        #print('Res apos do split', res +"hehe" )
        return res

    def clean_date(self, date):
        if(date == ""):
            return ""
        date = str(date)
        
        if(len(date)==8): #caso .br 
            year = date[0:4]
            month = date[4:6]
            day = date[6:8]
            return year +"-"+month+"-"+day
        if('T' in date): #caso internacional
            onlyDate = date.split('T')[0].split("-")
            year = onlyDate[0]
            month = onlyDate[1]
            day = onlyDate[2]
            return year +"-"+month+"-"+day

    def get_date_diff(self,d1,d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    def get_registry_data(self,url):
        #LOG_FILENAME =  'logRegistryFeatures' + '.log'
        #logging.basicConfig(filename=LOG_FILENAME, filemode ='w',level=logging.WARNING)
        #try:
        registry_data = dict()
        domain = self.get_main_domain_from_url(url)
        if(domain=='acidadeon.com'):
            registry_data['domain_registrar_url'] = 'http://tucowsdomains.com'
            registry_data['domain_update_date'] = '2021-09-02'
            registry_data['domain_creation_date'] = '2015-10-29'
            registry_data['domain_expiry_date'] = '2022-10-29'
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
            return registry_data

        if(domain=='avozdacidade.com'):
            registry_data['domain_registrar_url'] = 'http://www.tucows.com'
            registry_data['domain_update_date'] = '2019-11-15'
            registry_data['domain_creation_date'] = '2002-11-14'
            registry_data['domain_expiry_date'] = '2029-11-14'
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
            return registry_data                

        if(domain=='revistaoeste.com'):
            registry_data['domain_registrar_url'] = 'http://www.tucows.com'
            registry_data['domain_update_date'] = '2020-12-23'
            registry_data['domain_creation_date'] = '2020-01-10'
            registry_data['domain_expiry_date'] = '2022-01-10'
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
            return registry_data      

        if(domain=='ln.is'):
            registry_data['domain_registrar_url'] = ''
            registry_data['domain_update_date'] = '2021-09-27'
            registry_data['domain_creation_date'] = '2002-03-21'
            registry_data['domain_expiry_date'] = '2026-03-21'
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
            return registry_data   

        if(domain=='tribunadeparnaiba.com'):
            registry_data['domain_registrar_url'] = ''
            registry_data['domain_update_date'] = '2021-05-19'
            registry_data['domain_creation_date'] = '2014-05-23'
            registry_data['domain_expiry_date'] = '2022-05-23'
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
            return registry_data   

        #Esses aqui botei manualmente pq meu IP estorou limite de queries

        

        
        
        whois_query = self.get_whois_query(domain)
        #print(whois_query.stdout)
    
        registrar_url_formats = [
                                ("Registrar URL: ","\n"),
                                ]
        registry_data['domain_registrar_url'] = self.attempt_entry_formats(registrar_url_formats, whois_query)
        #print(registry_data)

        update_date_formats =[
                            ("Updated Date: ","\n"),
                            ("\nchanged:","\n")
                            ] 
        registry_data['domain_update_date'] = self.clean_date(self.attempt_entry_formats(update_date_formats, whois_query))
        #print(registry_data)

        creation_date_formats =[
                            ("Creation Date: ","\n"),
                            ("\ncreated:","\n")
                            ] 
        registry_data['domain_creation_date'] = self.clean_date(self.attempt_entry_formats(creation_date_formats, whois_query))
        #print(registry_data)

        expiry_date_formats =[
                            ("Registry Expiry Date: ","\n"),
                            ("Expiration Date: ","\n"),
                            ("expires:","\n")
                            ]
        registry_data['domain_expiry_date'] = self.clean_date(self.attempt_entry_formats(expiry_date_formats, whois_query))

        if(registry_data['domain_creation_date'] != ''):
            registry_data['domain_days_since_creation'] = self.get_date_diff(registry_data['domain_creation_date'], datetime.today().strftime("%Y-%m-%d"))
        else:
            registry_data['domain_days_since_creation'] = ''
        if(registry_data['domain_expiry_date'] != ''):
            registry_data['domain_days_until_expiry'] = self.get_date_diff(registry_data['domain_expiry_date'], datetime.today().strftime("%Y-%m-%d"))
        else:
            registry_data['domain_days_until_expiry'] = ''
        if(registry_data['domain_update_date'] != ''):
            registry_data['domain_days_since_last_update'] = self.get_date_diff(registry_data['domain_update_date'], datetime.today().strftime("%Y-%m-%d"))
        else:
            registry_data['domain_days_since_last_update'] = ''
        print(domain)
        print(registry_data)
        return registry_data
        #except:
            #logging.exception("ERROR: DOMINIO"+ domain +"\n")
            

if __name__ == "__main__":
    testing = RegistryFeaturesExtractor()
    # dfSubdomainSourceFeatures = pd.read_pickle('dfSubdomainSourceFeatures25Sep2021.pkl')
    # urlList = list(dfSubdomainSourceFeatures['subdomain'])
    # results = []
    # for url in urlList:
    #     results.append(testing.get_registry_data(url))

    # print("Final\n\n\n\n")
    # for a in results:
    #     print(a)

    res = testing.get_registry_data("tribunadeparnaiba.com")
    print(res)
