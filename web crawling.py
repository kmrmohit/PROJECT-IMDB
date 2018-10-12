
from lxml import html
from bs4 import BeautifulSoup
import requests
import time

start_page = requests.get('https://itunes.apple.com/us/app/candy-crush-saga/id553834731')
soup = BeautifulSoup(start_page.text,'html.parser')
print(soup.prettify())
"""

class AppCrawler:

    def __init__(self,starting_url,depth):
         self.starting_url = starting_url
         self.depth=depth
         self.current_depth = 0
         self.depth_links = []
         self.apps = []

    def crawl(self):
        app = self.get_app_from_link(self.starting_url)
        self.apps.append(app)
        self.depth_links.append(app.links)

        while self.current_depth < self.depth:
            current_links =[]
            for link in self.depth_links[self.current_depth]:
                current_app = self.get_app_from_link(link)
                current_links.extend(current_app.links)
                self.apps.append(current_app)
                time.sleep(5)
            self.current_depth +=1
            self.depth_links.append(current_links)
        return

    def get_app_from_link(self,link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)
        name = tree.xpath('//h1[@class="product-header__title app-header__title"]/text()')[0]
        description = tree.xpath('//h2[@class="product-header__subtitle app-header__subtitle"]/text()')[0]
        links = tree.xpath('//div[@id="ember110"]//a[@id="ember267"]/@href')
        
        app = App(name,description,links)
        return app

class App:
    
    def __init__(self,name,developer,links):
        self.name=name
        self.developer=developer
        self.links=links

    def __str__(self):
        return("Name: " +str(self.name.encode('UTF-8')) +
               "\r\nDeveloper: " + str(self.developer.encode('UTF-8'))+
               "\r\n")


crawler = AppCrawler('https://itunes.apple.com/us/app/candy-crush-saga/id553834731',3)
crawler.crawl()
for app in crawler.apps:
    print (app)
"""

    
