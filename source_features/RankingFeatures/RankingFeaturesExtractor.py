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
from fake_useragent import UserAgent

class BaseScrapper():
    def __init__(self, browser="chrome_headless"):
        self.set_selenium_driver(browser)

    def set_selenium_driver(self, browser="chrome_headless"):
        # Browser headless, for automatic executiond
        if browser == "chrome_headless":
            driver_dir = "../drivers/chromedriver"
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

        ua = UserAgent()
        userAgent = ua.random
        chrome_options.add_argument(f'user-agent={userAgent}')

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
    
    def get_domain_from_url(self,url):
        domain = url.split("://")[1].split("/")[0]
        domain.replace("www.", "")
        return domain

    def get_alexa_ranking(self,url):
        domain = self.get_domain_from_url(url)
        self.driver.get("https://www.alexa.com/siteinfo/" + domain)
        rankingElement = self.driver.find_element(*(By.XPATH,"//div[contains(@class, 'rankmini-rank') and span]"))
        rankingString = rankingElement.text.replace("#", "").replace(",", "")
        return int(rankingString)


    # def get_similarweb_ranking(self,url):
    #     domain = self.get_domain_from_url(url)
    #     self.driver.get("https://www.similarweb.com/website/" + domain)
    #     time.sleep(10)
    #     with open('filename.txt', 'w') as f:
    #         f.write(self.driver.page_source)


     
    #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "websiteRanks-container")))
        

    #     #time.sleep(10)




    #     rankingElement = self.driver.find_element(*(By.XPATH, "//li[contains(@class, 'js-globalRank')]/div[contains(@class,'websiteRanks-valueContainer')]"))          #"]")) #]
    #     rankingString = rankingElement.text.replace(",", "")
    #     return int(rankingString)


a = RankingFeaturesExtractor(0)
r0 = a.get_similarweb_ranking("https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19")
print(r0)
#r = a.get_alexa_ranking("https://diariodopoder.com.br/coronavirus/revisao-de-estudos-sobre-ivermectina-indica-eficacia-potencial-contra-covid-19")
