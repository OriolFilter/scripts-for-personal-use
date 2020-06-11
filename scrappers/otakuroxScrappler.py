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

        self.url=url
        self.word=word


    def searchElements(self):
        print('Searching:',self.word,'\n')
        link = "http://www.otakurox.com/directorio-series?q="+self.word.replace(' ','+') #sanitize_word
        # es pot fer servir
        # col-xs-12 col-sm-6 col-lg-6 (div, conté els elements)
        # or
        # <!--contenido cards--> (marca l'inici del div)

        # elements
        # col-xs-6 col-sm-4 col-md-3 col-lg-3 indi_rox

        http = urllib3.PoolManager()
        html_page = http.request('GET', link)
        # print(html_page.status)
        # print(html_page.datas)
        if html_page.status is 200:
            parser = BeautifulSoup(html_page.data, 'html.parser')
            # print(parser)
            self.aviableContainers=[]
            for element in parser.findAll('figure'):
                self.aviableContainers.append(element.findParent())

        html_page.release_conn()

    def printElements(self):
        x=0
        for container in self.aviableContainers:
            print(str(x)+' '*(3-len(str(x)))+ container.find('span').contents[0],
                  ' ' * (15 - len(container.find('span').contents[0])), container.get('title'))
            x += 1

    def selectElement(self,value):
        #Selecting which 'container' download
        return (self.getDownloadLinkFolder('www.otakurox.com'+self.aviableContainers[value].get('href')))


    def getDownloadLinkFolder(self,dlLink):
        link=None

        http = urllib3.PoolManager()
        html_page = http.request('GET', dlLink)
        if html_page.status is 200:
            parser = BeautifulSoup(html_page.data, 'html.parser')
            # print(parser)

            for element in parser.findAll('a'):
                if element.get('href') is None:pass
                elif '/descargar/' in element.get('href'):
                    link='http://www.otakurox.com'+element.get('href')
        html_page.release_conn()
        return link

    def getDownloadLinkList(self,dlLink):
        link=None
        print(dlLink)
        http = urllib3.PoolManager()
        html_page = http.request('GET', dlLink)
        if html_page.status is 200:
            parser = BeautifulSoup(html_page.data, 'html.parser')
            # print(parser)
            self.dlList = []
            #Ej [[nº Eps],[mega/mediafire],[lang],[uploader],[quality],[link]]
            table = parser.find(id='ddtt').find('tbody')
            # print('>',table.contents)
            x=0
            for tr in table.findAll('tr'):
                tdList=tr.findAll('td')
                self.dlList.append([[]])
                self.dlList[x][0]=(tdList[0].contents[0])
                self.dlList[x].append(tdList[1].find('span').contents[0])
                self.dlList[x].append(tdList[2].find('span').contents[0])
                self.dlList[x].append(tdList[3].contents[0])
                if tdList[len(tdList)-2].contents[0].get('href')[0] is '/': self.dlList[x].append('http://www.otakurox.com'+tdList[len(tdList)-2].contents[0].get('href'))
                else:self.dlList[x].append(tdList[len(tdList)-2].contents[0].get('href'))

                x+=1
            print(self.dlList)
        html_page.release_conn()
        return link

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
        downloadPath=''.join([self.StoragePath,album,"/",os.path.basename(url)]).replace("%2C",",").replace("%20"," ").replace("%21","!").replace("%26","&").replace("%27","'").replace("%28","(").replace("%29",")").replace("%E3%83%BB","・").replace("%EF%BC%8F","／")
        http = urllib3.PoolManager()
        file = http.request('GET',url,preload_content=False)
        with open(downloadPath, 'wb') as out:
            data = file.read()
            out.write(data)
        file.release_conn()


if 1 is 1: #Search by word
    print('Introdueix el nom de la serie a buscar:')
    # word=input()
    word='Ao no Exorcist'
    if word is not None and word is not '':
        test=parseData(word=word)
        test.searchElements()
        if len(test.aviableContainers) > 0:
            test.printElements()
            # print('\nIntrodueix un nombre per a seleccionar un element')
            # elementNumber=input()
            dlFolder=test.selectElement(value=1)
            test.getDownloadLinkList(dlFolder)
            # test.selectElement(value=elementNumber)
            # print(test.getDownloadLinkFolder(dlLink='http://www.otakurox.com/info/anime/416/ao-no-exorcist'))

        else: print('No s\'ha pogut trobar cap element amb el nom introduït')
        #pot mostrar un màxim de 63 elements??
    else: print('Has d\'introduïr algo')