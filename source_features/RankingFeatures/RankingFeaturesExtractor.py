import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
import tldextract
#from fake_useragent import UserAgent

class BaseScrapper():
    def __init__(self, browser="chrome_headless"):
        self.set_selenium_driver(browser)

    def set_selenium_driver(self, browser="chrome_headless"):
        # Browser headless, for automatic executiond
        if browser == "chrome_headless":
            driver_dir = "/home/joaomcouto/git/E02_features/source_features/drivers/chromedriver"
            print(driver_dir)
            chrome_options = self.__set_chrome_options()
            self.driver = webdriver.Chrome(options=chrome_options,
                                           executable_path=driver_dir)
        # Browser for visual execution
        elif browser == "firefox":
            driver_dir = "../drivers/geckodriver"
            self.driver = webdriver.Firefox(executable_path=driver_dir)

    def __set_chrome_options(self):
        """
        Set arguments for headless chome.
        """
        chrome_options = Options()

#         ua = UserAgent()
#         userAgent = ua.random
#         chrome_options.add_argument(f'user-agent={userAgent}')

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')

        return chrome_options

class RankingFeaturesExtractor(BaseScrapper):
    def __init__(self,interface):
        if interface:
            super(RankingFeaturesExtractor, self).__init__(browser="firefox")
        else:
            super(RankingFeaturesExtractor, self).__init__()

    def get_alexa_ranking(self,url):
        
        ext = tldextract.extract(url)
        subdomain ='.'.join(part for part in ext if part)
        
        self.driver.get("https://www.alexa.com/siteinfo/" + subdomain)
        rankingElement = self.driver.find_element(*(By.XPATH,"//div[contains(@class, 'rankmini-rank') and span]"))
        rankingString = rankingElement.text.replace("#", "").replace(",", "")
        return int(rankingString)
        
    def get_domcop_10million_rank(self,url,dfTenMill):
        ext = tldextract.extract(url)
        subdomain ='.'.join(part for part in ext if (part and part!='www'))    
        return dfTenMill[dfTenMill['Domain'] == subdomain]['Rank'].values[0]
    
    def get_domcop_10million_open_page_rank(self,url,dfTenMill):
        ext = tldextract.extract(url)
        subdomain ='.'.join(part for part in ext if (part and part!='www'))
        return dfTenMill[dfTenMill['Domain'] == subdomain]['Open Page Rank'].values[0]
        
        
    def get_ranking_data(self,url, dfTenMill):
        ranking_data = dict()
        #ranking_data['subdomain_alexa_ranking'] = self.get_alexa_ranking(url)
        ranking_data['subdomain_tenMill_rank'] = self.get_domcop_10million_rank(url,dfTenMill)
        ranking_data['subdomain_tenMill_open_page_rank'] =self.get_domcop_10million_open_page_rank(url,dfTenMill)
        return ranking_data
    
if __name__ == "__main__":
    a = RankingFeaturesExtractor(0)

    r = a.get_alexa_ranking("https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19")
    print(r)
    
    a.testing()


