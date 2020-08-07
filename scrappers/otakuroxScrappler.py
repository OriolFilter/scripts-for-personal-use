# Will avoid use Otakurox, since animeflv is more consistent

import os
from bs4 import BeautifulSoup
import urllib3
from time import sleep
import pathlib
from selenium import webdriver

driverFolder=str(pathlib.Path(__file__).parent)+"/driversFolder"
firefox64b=driverFolder + '/geckodriver64x'
firefox32b=driverFolder + '/geckodriver32x' #NoEsta


# import os
# os.system()
#
#
#
#


storingFolder='/tmp/animuTest/'
class downloadManager:
    def __init__(self,albumName,dlLink):
        print(albumName)
        self.albumName:str=albumName.replace('\\',' ').replace('/',' ')
        self.dlLink:str=dlLink


    def createFolder(self):
        try:
            os.mkdir(storingFolder+self.albumName)
        except OSError as e:print(e)

    def downloadMega(self):
        self.dlLink.replace('/folder/','/#F!').replace('#','!')
        file = open(storingFolder+self.albumName+"/link", "w")
        file.write(self.dlLink)
        file.close()

    def downloadLik(self):
        pass
        if 'mega.nz/' in self.dlLink:self.downloadMega()
        elif 'drive.google.com/' in self.dlLink:pass


class shortener:
    def __init__(self,link):
        self.link=link
        self.downloadLink=None

    def getShortenedLink(self):
        web = webdriver.Firefox(executable_path=firefox64b)
        web.get(self.link)
        sleep(4)
        self.dllink = web.current_url
        web.close()

        if 'adfly' in self.link: print('adfly it\'s not supported')
        else: self.ouo()
        return (self.downloadLink)

    def ouo(self):
        # print('ouo')
        # print(self.dllink)
        web = webdriver.Firefox(executable_path=firefox64b)
        web.get(self.dllink)
        sleep(3)
        web.execute_script("document.forms[0].submit()")
        sleep(5)
        web.execute_script("document.forms[0].submit()")
        sleep(5)
        self.downloadLink=web.current_url
        web.close()


    def adfly(self):pass

class parseDataOtakurox:
    def __init__(self,StoragePath=None,url=None,word=None,mode=0):

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
            self.aviableContainersList=[]
            x=0
            for element in parser.findAll('figure'):
                self.aviableContainersList.append([[]])
                self.aviableContainersList[x][0]=element.findParent().find('span').contents[0]
                self.aviableContainersList[x].append(element.findParent().get('title'))
                self.aviableContainersList[x].append(element.findParent().get('href'))
                x+=1
        html_page.release_conn()

    def printElements(self):
        x=0
        # print(self.aviableContainersList)
        for container in self.aviableContainersList:
            print(str(x)+' '*(3-len(str(x)))+ container[0],
                  ' ' * (15 - len(container[0])), container[1])
            x += 1


    def selectElement(self,value):
        #Selecting which 'container' download
        self.albumName=self.aviableContainersList[value][1]
        return self.getDownloadLinkFolder('www.otakurox.com'+self.aviableContainersList[value][2])

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

    def getDownloadLinkList(self,dlLink,type=None):
        link=None
        http = urllib3.PoolManager()
        html_page = http.request('GET', dlLink)
        if html_page.status is 200:
            parser = BeautifulSoup(html_page.data, 'html.parser')
            self.aviableDownloadLinkList = []
            table = parser.find(id='ddtt').find('tbody')
            x=0
            for tr in table.findAll('tr'):
                tdList=tr.findAll('td')
                if (type is 'mega' and tdList[1].find('span').contents[0].lower() == 'mega') or (type is None):
                    self.aviableDownloadLinkList.append([[]])
                    self.aviableDownloadLinkList[x][0]=(tdList[0].contents[0])
                    self.aviableDownloadLinkList[x].append(tdList[1].find('span').contents[0])
                    self.aviableDownloadLinkList[x].append(tdList[2].find('span').contents[0])
                    self.aviableDownloadLinkList[x].append(tdList[5].find('a').contents[0])
                    self.aviableDownloadLinkList[x].append(tdList[6].contents[0])
                    if tdList[len(tdList)-2].contents[0].get('href')[0] is '/': self.aviableDownloadLinkList[x].append('http://www.otakurox.com'+tdList[len(tdList)-2].contents[0].get('href'))
                    else:self.aviableDownloadLinkList[x].append(tdList[len(tdList)-2].contents[0].get('href'))
                    x += 1



        html_page.release_conn()
        return link

    def printDownloadLinkList(self):
        x=0
        print()
        for info in self.aviableDownloadLinkList:
            # print(info)
            print(str(x)+' '*(3-len(str(x)))+info[0]+' ' * (17 - len(info[0]))+info[1]+' ' * (15 - len(info[1]))+info[2]+' ' * (15 - len(info[2]))+info[3]+' ' * (15 - len(info[3]))+info[4]+' ' * (15 - len(info[4]))+info[5])
            x += 1

    def selectDownloadOption(self,value):
        #Selecting which 'Download List' download
        return self.aviableDownloadLinkList[value][5]


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




optionMenu=1

# if optionMenu is 1: #Search by word
#     print('Introdueix el nom de la serie a buscar:')
#     word = input()
#     # word='Ao no Exorcist'
#     if word is not None and word is not '':
#         parse = parseDataOtakurox(word=word,mode=0)
#         parse.searchElements()

# elif optionMenu is 1:  # Search by word
if optionMenu is 1:  # Search by word
    print('Introdueix el nom de la serie a buscar:')
    word=input()
    # word='Ao no Exorcist'
    if word is not None and word is not '':
        parse=parseDataOtakurox(word=word)
        parse.searchElements()
        if len(parse.aviableContainersList) > 0:
            parse.printElements()
            print('\nIntrodueix un nombre per a seleccionar un element')
            elementNumber=int(input())
            dlFolder=parse.selectElement(value=elementNumber)
            parse.getDownloadLinkList(dlFolder,type='mega')
            if len(parse.aviableDownloadLinkList) > 0:
                parse.printDownloadLinkList()
                print('\nIntrodueix un nombre per a seleccionar un element')
                elementNumber=int(input())
                dlLink = parse.selectDownloadOption(value=elementNumber)
                dlManagerLink = shortener(link=dlLink)
                dlManagerLink.getShortenedLink()
                parse2=downloadManager(albumName=parse.albumName,dlLink=dlManagerLink.downloadLink)
                parse2.createFolder()
                parse2.downloadMega()
                # print(parse.getDownloadLinkFolder(dlLink='http://www.otakurox.com/info/anime/416/ao-no-exorcist'))
            else: print('No s\'ha pogut trobar cap element amb l\'opcio seleccionada')
        else: print('No s\'ha pogut trobar cap element amb el nom introduït')
        #pot mostrar un màxim de 63 elements??
    else: print('Has d\'introduïr algo')
elif optionMenu is 2: #Download matching words
    print('Introdueix el nom per a filtrar i descarregar els que coincideixin:')
    word=input()
    # word='Ao no Exorcist'
    if word is not None and word is not '':
        parse=parseDataOtakurox(word=word)
        parse.searchElements()
        if len(parse.aviableContainersList) > 0:
            parse.printElements()
            # print('\nIntrodueix un nombre per a seleccionar un element')
            # elementNumber=int(input())
            x=0
            for element in parse.aviableContainersList:
                dlFolder=parse.selectElement(value=x)
                if dlFolder is not None:
                    print(parse.albumName)
                    parse.getDownloadLinkList(dlFolder,type='mega')
                    # parse.printDownloadLinkList()
                    if len(parse.aviableDownloadLinkList) > 0:
                        # parse.printDownloadLinkList()
                        elementNumber = 0
                        dlLink = parse.selectDownloadOption(value=elementNumber)
                        dlManagerLink = shortener(link=dlLink)
                        dlManagerLink.getShortenedLink()
                        parse2 = downloadManager(album=parse.albumName, dlLink=parse.downloadLink)
                        parse2.createFolder()
                        parse2.downloadMega()
                    else: print('No s\'ha pogut trobar cap element amb l\'opcio seleccionada')
                else: print('No s\'ha pogut trobar cap element amb l\'opcio seleccionada')
                x+=1


                # print(parse.getDownloadLinkFolder(dlLink='http://www.otakurox.com/info/anime/416/ao-no-exorcist'))
        else: print('No s\'ha pogut trobar cap element amb el nom introduït')
        #pot mostrar un màxim de 63 elements??
    else: print('Has d\'introduïr algo')