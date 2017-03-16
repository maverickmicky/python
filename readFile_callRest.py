# Script to read a csv file of some ids and then call a rest api with id as param. input arg is required to provide baseurl for rest service
import sys
import urllib2
import csv
import logging
import time
import xml.etree.ElementTree as ET

BASE_URL=sys.argv[1]
SUCCESS_COUNT = 0
UNSUCCESS_COUNT = 0

logger = logging.getLogger("sessionLogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

generalLogFileHandler = logging.FileHandler("serverSession.log")
generalLogFileHandler.setLevel(logging.INFO)
generalLogFileHandler.setFormatter(formatter)

errorLogFileHandler = logging.FileHandler("serverSessionError.log")
errorLogFileHandler.setLevel(logging.ERROR)
errorLogFileHandler.setFormatter(formatter)

logger.addHandler(generalLogFileHandler)
logger.addHandler(errorLogFileHandler)

logger.info("start")

def sendToSERVER(serverSessionId):
        url = '{0}/service/sessionId/{1}'.format(BASE_URL,serverSessionId)
        logger.info("Sending to SERVER, url: %s", url)

        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)

        req = urllib2.Request(url, headers={"Content-Type":"text/xml"})

        time.sleep(0.100)
        try:
                res = opener.open(req)
                code = ET.parse(res).getroot().find('Outcome').get('code')
                if code == '0':
                        logger.info("SessionId %s : ResponseCode %s", serverSessionId, code)

                        global SUCCESS_COUNT
                        SUCCESS_COUNT = SUCCESS_COUNT + 1
                else:
                        logger.error("SessionId %s : ResponseCode %s", serverSessionId, code)

                        global UNSUCCESS_COUNT
                        UNSUCCESS_COUNT = UNSUCCESS_COUNT + 1
        except urllib2.HTTPError as e:
                logger.error("SessionId %s : HTTP Error %s", serverSessionId, e.code)

#                global UNSUCCESS_COUNT
                UNSUCCESS_COUNT = UNSUCCESS_COUNT + 1

                pass

with open('input.txt','rb') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
                if row:
                        sendToSERVER(row[0])

logger.info("SUCCESS_COUNT: %s", SUCCESS_COUNT)
logger.info("UNSUCCESSFULL_COUNT: %s", UNSUCCESS_COUNT)
logger.info("end")