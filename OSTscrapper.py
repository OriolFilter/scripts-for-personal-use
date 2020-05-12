import os
import time

from bs4 import BeautifulSoup
import urllib3


#mp3 or flac?
#flac + cualité -> ocupa mes
StorageFolder="/tmp/"
AdditionalWord=" OST"
class parseData:
    def __init__(self,StoragePath=None,url=None,word=None,additionalWord=None):
        if word is None:
            self.StoragePath = ''.join([StoragePath,"/"])
        else:
            self.StoragePath=''.join([StoragePath,word,AdditionalWord,"/"])
        self.url=url
        self.word=word

    def getAlbum(self):
        #Falta descarregar imatges tambe
        http = urllib3.PoolManager()
        html_page = http.request('GET', self.url)
        # print(html_page.status)
        if html_page.status is 200:
            # Dins album
            album = BeautifulSoup(html_page.data, 'html.parser')
            lastLink = None
            AlbumTitle = album.find('h2').contents[0]
            if not os.path.isdir(''.join([self.StoragePath,AlbumTitle])):
                # os.mkdir(self.StoragePath+AlbumTitle)
                os.makedirs(''.join([self.StoragePath,AlbumTitle]),exist_ok=True)
            print('>', AlbumTitle)
            #Descarregar mp3
            for link in album.findAll('a'):
                if lastLink != link.get('href'):
                    if link.get('href') is None:
                        pass
                    elif link.get('href').startswith('/') and link.get('href').endswith('.mp3'):
                        # print(link.get('href'))
                        # AconseguirElLinkDelMP3
                        mp3PageHtml = http.request('GET',''.join(["https://downloads.khinsider.com",link.get('href')]))
                        mp3PageHtmlContent = BeautifulSoup(mp3PageHtml.data, 'html.parser')
                        downloadButtons = mp3PageHtmlContent.find_all('span', class_='songDownloadLink')
                        for file in downloadButtons:
                            if file is None: pass
                            else:
                                linkFile = file.find_previous().get('href')
                                self.downloadFile(linkFile,AlbumTitle)

                        mp3PageHtml.release_conn()
                lastLink = link.get('href')
            #Descarregar img/covers
            contentTable = album.find('table', class_='contentpaneopen')
            for img in contentTable.find('table').findAll('img'):
                self.downloadFile(url=img.get('src'),album=AlbumTitle)
        html_page.release_conn()
    def searchAlbum(self):
        sanitizedName = self.word.lower().replace(" ", "").replace("-", "").replace("_", "").replace(",", "")
        # print(sanitizedName)
        http = urllib3.PoolManager()
        html_page = http.request('GET', self.url)
        if html_page.status is 200:
            SearchHtml = BeautifulSoup(html_page.data, 'html.parser')
            for link in SearchHtml.findAll('a'):
                if link.contents is None:
                    pass
                else:
                    # print(link.contents[0])
                    sanitizedLink = str(link.contents[0]).lower().replace(" ", "").replace("-", "").replace("_","").replace(",", "")
                    if sanitizedName in sanitizedLink:
                        self.url=''.join(["https://downloads.khinsider.com/",link.get('href')])
                        self.getAlbum()

    def downloadFile(self,url,album=None):
        downloadPath=''.join([self.StoragePath,album,"/",os.path.basename(url)]).replace("%20"," ")
        http = urllib3.PoolManager()
        file = http.request('GET',url,preload_content=False)
        with open(downloadPath, 'wb') as out:
            data = file.read()
            out.write(data)
        file.release_conn()



Opcions1={
    1:{
        "source":"Download from khinsider.com",
        "link":"khinsider.com"
    },
    2:{
        "source":"Download from thehylia.com",
        "link":"thehylia.com"
       }
} #

Opcions2={
    "khinsider.com":
        {
        1:"Download album from X url",
        2:"Download albums that match X string start (ex, 'Pok', match with all the Pokemon albums)"
        },
    "thehylia.com":
        {
        1: "Nothing"
        }
}


print("Selecciona una d'aquestes opcions")

for opcions in Opcions1:
    print(''.join([str(opcions)," ",str(Opcions1[opcions]['source'])]))
webpage=int(input())

print("Selecciona una d'aquestes opcions")

for opcions in Opcions2[Opcions1[webpage]["link"]]:
    print(''.join([str(opcions)," ",str(Opcions2[Opcions1[webpage]["link"]][opcions])]))
action=int(input())


if webpage is 1:
    if action is 1:
        print('Introduce the url to download from')
        # url='https://downloads.khinsider.com/game-soundtracks/album/guilty-gear-2-overture-vol.1'
        url = input()
        item = parseData(StoragePath=StorageFolder, url=url, word=None)
        item.getAlbum()
    elif action is 2:
        print('Introduce the word to filter (the input will also be used to create a folder to put the items)')
        word = input()
        item = parseData(StoragePath=StorageFolder,url=''.join(["https://downloads.khinsider.com/game-soundtracks/browse/",word[0].upper()]), word=word,additionalWord=AdditionalWord)
        item.searchAlbum()
    else:
        print('Wrong input!')
elif webpage is 2:
    if action is 1:
        pass
else:
    print('Wrong input!')

print('The end')

# from here? https://downloads.khinsider.com/


    # https://docs.python.org/3/library/urllib.request.html#module-urllib.request