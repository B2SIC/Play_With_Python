from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import datetime


class GBus():
    def __init__(self, keyword):
        self.API_KEY = ""
        self.TEST_KEY = "1234567890"

        routeStationDownloadUrl = "http://openapi.gbis.go.kr/ws/rest/baseinfoservice?serviceKey=" + self.TEST_KEY
        getStationIdUrl = "http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=" + self.TEST_KEY + "&keyword=" + parse.quote(keyword)

        self.stationList = []
        page = urlopen(getStationIdUrl).read()
        soup = BeautifulSoup(page, 'lxml')
        regionName = soup.findAll("regionname")
        stationId = soup.findAll("stationid")
        stationName = soup.findAll("stationname")

        for e in range(len(stationId)):
            self.stationList.append("^(" + regionName[e].string + ") " + stationName[e].string + "-" + stationId[e].string)
            
    def stationSender(self, rawString):
        return self.getBusList(myStationId)
        
    def getBusList(self, rawString):
        mId = rawString.split("-")[1]
        
        outputData = ""

        dt = datetime.datetime.now()
        cvt = dt.strftime("%Y%m%d")
        getMatchingFile = "http://openapi.gbis.go.kr/ws/download?routestation" + cvt + ".txt"
        fileData = urlopen(getMatchingFile).read().decode('UTF-8').split("^")
        # print(fileData)

        getBusUrl = "http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=" + self.API_KEY + "&stationId=" + mId
        page = urlopen(getBusUrl).read()
        soup = BeautifulSoup(page, 'lxml')
        routeIdList = soup.findAll("routeid")
        stationIdList = soup.findAll("stationid")
        locationNo1 = soup.findAll("locationno1")
        locationNo2 = soup.findAll("locationno2")
        predictTime1 = soup.findAll("predicttime1")
        predictTime2 = soup.findAll("predicttime2")

        for e in range(len(routeIdList)):
            matchingString = routeIdList[e].string + "|" + stationIdList[e].string
            for item in fileData:
                if matchingString in item:
                    itemSplit = item.split("|")
                    outputData += itemSplit[4] + "번 버스 약 " + predictTime1[e].string + "분 후에 도착" + "(" + locationNo1[e].string + "번째 전)\n"

        if outputData == "":
            return "운행 중인 버스 정보를 찾을 수 없습니다."
        else:
            return "[버스 도착 안내 서비스]\n\n" + outputData
