import os

dbPath = '/var/tmp/'

class simpleDB(object):
    def __init__(self, dbFileName):
        self._db = dbPath+dbFileName

    def read(self):
        dbDict={}
        if os.path.exists(self._db):
            with open(self._db) as myFile:
                for eachLine in myFile:
                     lineSp = eachLine.split(':::')
                     dbDict[lineSp[0]]=lineSp[1].rstrip('\n')
        return dbDict

    def write(self, dataDict):
        oldData=self.read()
        #print('SKM', oldData)
        fHandle = open(self._db, 'w+')
        fDict={}
        for key, data in oldData.items():
            fDict[key]=data
        for key, data in dataDict.items():
            fDict[key]=data
        for key, data in fDict.items():
            fHandle.write(key+':::'+data+'\n')
        fHandle.close()
