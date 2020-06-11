import os
import time

from bs4 import BeautifulSoup
import urllib3
import requests

class parseData:
    def __init__(self,StoragePath=None,url=None,word=None,additionalWord=None,link=None):
        self.url=link
    def getOuoLink(self):
        print('start')
        # print(sanitizedName)#Part1
        http = urllib3.PoolManager()
        html_page = http.request('GET', self.url)
        print(html_page.data)
        if html_page.status is 200:
            SearchHtml = BeautifulSoup(html_page.data, 'html.parser')
            for link in SearchHtml.findAll('form'):
                if link is None:
                    pass
                else:
                    nextLink=link.get('action')
                    print(nextLink)
                    # self.url =''.join(["https://downloads.khinsider.com/" ,link.get('href')])
                    # self.getAlbum()

        else: print("f")



test=parseData(link="http://avi.im/stuff/js-or-no-js.html")
# test=parseData(link="https://ouo.io/IzSiJq")
test.getOuoLink()


#Sora https://mega.nz/folder/mZ5kVCaB#yGxMLYH5tZYJDOIne58E8Q

# POST https://docs.akana.com/cm/api_oauth/oauth_oauth20/m_oauth20_getTokenPOST.htm
# POST https://auth0.com/docs/flows/guides/auth-code/call-api-auth-code