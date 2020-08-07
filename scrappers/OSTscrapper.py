import os
import time

from bs4 import BeautifulSoup
import urllib3


#mp3 or flac?
#flac + cualité -> ocupa mes
StorageFolder="/tmp/OST/"
AdditionalWord=" OST"
class parseData:
    # Misc
    def __init__(self,StoragePath=None,word=None,additionalWord=None):
        # CrearDirectori, millorar, fer al descarregar, no al buscar
        if word is None:
            self.StoragePath = ''.join([StoragePath,"/"])
        else:
            self.StoragePath=''.join([StoragePath,word,additionalWord,"/"])
        self.word=word
        self.wordS=self.sanitizeWord(word)

    def sanitizeWord(self,word):return word.lower().replace(" ", "").replace("-", "").replace("_", "").replace(",", "") # Fa falta afegir accents
    def downloadFile(self,url,album=None):
        downloadPath=''.join([self.StoragePath,album,"/",os.path.basename(url)]).replace("%2C",",").replace("%20"," ").replace("%21","!").replace("%26","&").replace("%27","'").replace("%28","(").replace("%29",")").replace("%E3%83%BB","・").replace("%EF%BC%8F","／")
        http = urllib3.PoolManager()
        file = http.request('GET',url,preload_content=False)
        with open(downloadPath, 'wb') as out:
            data = file.read()
            out.write(data)
        file.release_conn()

    # Khinsider
    def getAlbum_khinsider(self,albumUrl):
        #Falta descarregar imatges tambe
        http = urllib3.PoolManager()
        html_page = http.request('GET', albumUrl)
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
    def searchAlbum_khinsider(self):
        sanitizedName = self.word.lower().replace(" ", "").replace("-", "").replace("_", "").replace(",", "")
        # print(sanitizedName)
        http = urllib3.PoolManager()
        html_page = http.request('GET', ''.join(["https://downloads.khinsider.com/game-soundtracks/browse/",self.word[0].upper()]))
        if html_page.status is 200:
            SearchHtml = BeautifulSoup(html_page.data, 'html.parser')
            for link in SearchHtml.findAll('a'):
                if link.contents is None:
                    pass
                else:
                    # print(link.contents[0])
                    sanitizedLink = str(link.contents[0]).lower().replace(" ", "").replace("-", "").replace("_","").replace(",", "")
                    if sanitizedName in sanitizedLink:
                        albumUrl=''.join(["https://downloads.khinsider.com/",link.get('href')])
                        self.getAlbum_khinsider(albumUrl=albumUrl)

    # TheHylia
    def searchAlbum_thehylia(self,mode=0):
        # Modes
        # 0 List and select
        # 1 Download all matching X
        # print(sanitizedName)
        http = urllib3.PoolManager()
        html_page = http.request('GET', ''.join(["https://anime.thehylia.com/soundtracks/browse/all"]))
        if html_page.status is 200:
            # SearchHtml = BeautifulSoup(html_page.data, 'html.parser')
            SearchHtml = BeautifulSoup(html_page.data, 'html.parser').find(id='main').find(attrs={'align':'left'})#.find() # Inside container
            x=0
            list={}
            # print(SearchHtml)
            # print(len(SearchHtml.findAll('a')))

            for link in (album for album in SearchHtml.findAll('a') if self.wordS in self.sanitizeWord(album.contents[0])):
                list[x]={"name":link.contents[0],
                           "href":link.get('href')
                }
                x+=1
            if len(list) is 0:
                print('0 elements found')
            else:
                if mode is 1: [self.getAlbum_thehyla(list[element]['href']) for element in list]
                    # for element in list: pass #self.downloadFile()
                elif mode is 0:
                    [print('{} : {}'.format(element, list[element]['name'])) for element in list]
                    print('\n\nSelect one option from the list')
                    # value = int(input()) # D
                    value = 0
                    if value >= 0 and value < len(list):
                        # print(value)
                        self.getAlbum_thehyla(list[value]['href'])
                    else: print('Quitting, value out of range...') # Quitting > Exitting right?

    def getAlbum_thehyla(self,albumUrl):
        # < meta name = "keywords" content = "anime, download, avi, mp3, music, media, mp3" >

        http = urllib3.PoolManager()
        html_page = http.request('GET', albumUrl)
        # print(html_page.status)
        if html_page.status is 200:

            # Dins album
            album = BeautifulSoup(html_page.data, 'html.parser')
            # lastLink = None
            AlbumTitle = album.find('h2').contents[0]
            # Crear Carpeta Album
            if not os.path.isdir(''.join([self.StoragePath, AlbumTitle])):
                # os.mkdir(self.StoragePath+AlbumTitle)
                os.makedirs(''.join([self.StoragePath, AlbumTitle]), exist_ok=True)
            print('>', AlbumTitle)
            # albumInfo = album.find(attrs={'id': 'main_container'}).find(attrs={'align': 'left'}) # Unused, when need to use it i will improve it # No c si funciona
            albumImgList = [link.get('href') for link in album.find(attrs={'id': 'main_container'}).findAll('a') if link.get('href').endswith('.jpg')]
            albumMp3List = [link.get('href') for link in album.find(name='table',attrs={'align':'center','width':'95%'}).findAll('a') if link.get('href').endswith('.mp3' or '.avi' or '.flac')] # Mp3/avi list, avi untested
            # Descarregar mp3/avi/flac
            for href in albumMp3List:
                # AconseguirElLinkDelMP3
                mp3PageHtml = http.request('GET',href)
                mp3PageHtmlContent = BeautifulSoup(mp3PageHtml.data, 'html.parser')
                [self.downloadFile(a.get('href'), album=AlbumTitle) for a in mp3PageHtmlContent.find_all('a') if a.get('href').endswith('.mp3' or '.avi' or '.flac')]
                # print([a.get('href') for a in mp3PageHtmlContent.find_all('a') if a.get('href').endswith('.mp3' or '.avi' or '.flac')])
                mp3PageHtml.release_conn()

            # Descarregar img/covers
            [self.downloadFile(href, album=AlbumTitle) for href in albumImgList]

                # print(href)
                # print(link)
            # for link in album.findAll('a'):
            #     if lastLink != link.get('href'):
            #         if link.get('href') is None:
            #             pass
            #         elif link.get('href').startswith('/') and link.get('href').endswith('.mp3'):
            #             # print(link.get('href'))
            #             mp3PageHtml = http.request('GET',link.get('href'))
            #             mp3PageHtmlContent = BeautifulSoup(mp3PageHtml.data, 'html.parser')
            #             downloadButtons = mp3PageHtmlContent.find_all('span', class_='songDownloadLink')
            #             for file in downloadButtons:
            #                 if file is None:
            #                     pass
            #                 else:
            #                     linkFile = file.find_previous().get('href')
            #                     # self.downloadFile(linkFile, AlbumTitle)
            #                     print(linkFile, AlbumTitle)
            #
            #             mp3PageHtml.release_conn()
            #     lastLink = link.get('href')
            # Descarregar img/covers
            # contentTable = album.find('table', class_='contentpaneopen')
            # for img in contentTable.find('table').findAll('img'):
            #     self.downloadFile(url=img.get('src'), album=AlbumTitle)
        html_page.release_conn()


Opcions={
    'text': [{
        1:{
            "source":"Download from khinsider.com",
            "link":"khinsider.com"
        },
        2:{
            "source":"Download from TheHylia.com",
            "link":"thehylia.com"
           }
    }],
    'actions': [{
        "khinsider.com":{
            1:"Download album from X url",
            2:"Download albums that match X string start (ex, 'Pok', match with all the Pokemon albums)"
            },
        "thehylia.com":{
            1: "Search word and select album to download",
            2: "Download all albums that match X word"
        }
    }]
}

print('------')
# print(Opcions['text'][0][1])
print("Selecciona una d'aquestes opcions")

for opcions in Opcions['text'][0]:
    print(''.join([str(opcions)," ",str(Opcions['text'][0][opcions]['source'])]))
# webpage=int(input()) # D
webpage=2

print("Selecciona una d'aquestes opcions")

for opcions in Opcions['actions'][0][Opcions['text'][0][webpage]["link"]]:
    print(''.join([str(opcions)," ",str(Opcions['actions'][0][Opcions['text'][0][webpage]["link"]][opcions])]))
# action=int(input())
action=2 # D


if webpage is 1:
    if action is 1:
        print('Introduce the url to download from')
        # url='https://downloads.khinsider.com/game-soundtracks/album/guilty-gear-2-overture-vol.1'
        albumUrl = input()
        item = parseData(StoragePath=StorageFolder, word=None)
        item.getAlbum_khinsider(album=albumUrl)
    elif action is 2:
        print('Introduce the word to filter (the input will also be used to create a folder to put the items)')
        word = input()
        item = parseData(StoragePath=StorageFolder, word=word,additionalWord=AdditionalWord)
        item.searchAlbum_khinsider()
    else:
        print('Wrong input!')
elif webpage is 2:
    if action is 1:
        print('Introduce the word to filter (the input will also be used to create a folder to put the items)')
        # word = input()
        word = 'Machine Doll wa Kizutsukanai OP Single - Anicca' # D
        item = parseData(StoragePath=StorageFolder,word=word, additionalWord=AdditionalWord)
        item.searchAlbum_thehylia()
    elif action is 2:
        print('Introduce the word to filter (the input will also be used to create a folder to put the items)')
        # word = input()
        word = 'Machine Doll' # D
        item = parseData(StoragePath=StorageFolder, word=word, additionalWord=AdditionalWord)
        item.searchAlbum_thehylia(mode=1)
    else:
        print('Wrong input!')
else:
    print('Wrong input!')

print('The end')

# from here? https://downloads.khinsider.com/


    # https://docs.python.org/3/library/urllib.request.html#module-urllib.request