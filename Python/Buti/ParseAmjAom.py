import requests
import re
from bs4 import BeautifulSoup

URLROOT = '''http://amj.aom.org'''
class Parseamjaom(object):
    
    def __init__(self,urlroot):
        self.urlroot = urlroot
        
    def __str__(self):
        return self.soup.prettify()

    def get_respnose(self,urlleaf):
        self.urlleaf = urlleaf
        self.fullurl = self.urlroot + self.urlleaf
        self.response = requests.get(self.fullurl)

    #def get_response_html(self)
        self.htmldoc  = self.response.text
        self.soup = BeautifulSoup(self.htmldoc, "html5lib")

    def get_articles_title(self):
        def has_cit_title_group_only(css_class):
            #filter
            #print css_class
            return css_class == "cit-title-group" and css_class != "cit-first-element"
            
        self.title = self.soup.find_all('h4',class_=has_cit_title_group_only,text=re.compile('^(?!Announcement)'))
        for h in self.title:
            yield h.get_text()
    
    def get_articles_abstract(self):
        self.abstract = self.soup.find_all('a',text='Abstract')
        
        for a in self.abstract:
            self.abstractlink = URLROOT + a.get('href')
            self.abstractpage = requests.get(self.abstractlink)
            self.abstractpagehtml = self.abstractpage.text
            self.abstractsoup = BeautifulSoup(self.abstractpagehtml,"html5lib")
            self.abstracttag = self.abstractsoup.find_all(id='p-1')
            for abstext in self.abstracttag:
                yield abstext.get_text()
    
if __name__ == '__main__':

    p = Parseamjaom(URLROOT)
    p.get_respnose('/content/38/3.toc')

    #get title start
    #titlegen =  p.get_articles_title()
    #for i in titlegen:
    #    print i
    #Get title end

    #Get abstract Start
    abstractgen = p.get_articles_abstract()
    for abstext in abstractgen:
        print abstext
    #Get abstract End