import sys
sys.path.append('./lib')
from smldb import simpleDB
import getpass
import bcrypt
import multiprocessing
from multiprocessing import Manager
parallel_thread=32

myDB=simpleDB('passwd.txt')
passDict=myDB.read()
userNm=getpass.getuser()

def getPass(pLen):
    #a-z:97-122,A-Z:65-90,0-9:48-57
    pList=[]
    for i in range(48,58):
        pList.append(chr(i))
    for i in range(65,91):
        pList.append(chr(i))
    for i in range(97,123):
        pList.append(chr(i))
    iList=[]
    for val in pList:
        iList.append(val)
    fList=[]
    if pLen > 1:
        for i in range(2,pLen+1):
            nList=[]
            for val in iList:
                ppwd=val
                for val in pList:
                    npwd=ppwd+val
                    nList.append(npwd)
            iList=[]
            for val in nList:
                iList.append(val)
    else:
        nList=iList
    return nList
                
def checkPass(chkPass, storedPass, storedHash, return_dict):
    passFound=False
    thisPass=bcrypt.hashpw(chkPass.encode(), storedHash.encode())
    if thisPass == storedPass.encode():
        passFound=True
    return_dict[chkPass]=passFound
    
def hackTry(pwdFile, hshFile):
    #Password in range of a-z,A-Z,0-9
    passLen=2
    tryPassList=getPass(passLen)
    totalPass=len(tryPassList)
    parallelRunCount=totalPass/parallel_thread
    stPos=0
    runCount=0
    print('Total possible passwords: ',totalPass)
    print('Parallelism: ',parallel_thread,' Loops:',parallelRunCount)
    tt=input('Hit a key to begin')
    while runCount < parallelRunCount:
        print('Run #',runCount,' of ',parallelRunCount)
        testList=tryPassList[stPos:stPos+parallel_thread]
        manager = Manager()
        return_dict=manager.dict()
        jobs=[]
        for eachPass in testList:
            process = multiprocessing.Process(target=checkPass, args=(eachPass, pwdFile, hshFile, return_dict))
            jobs.append(process)
        for j in jobs:
            j.start() 
        for j in jobs:
            j.join()
        print('SKM jobs done')
        for eachPass in testList:
            if return_dict[eachPass]:
                print('Cracked the password for user: '+userNm+', it is: '+eachPass)
                sys.exit(0)
            else:
                print(eachPass+': Not right password')
        stPos+=parallel_thread
        runCount+=1
    #for eachPass in tryPassList:
    #    print('Trying password ',eachPass)
    #    pwdCorrect=checkPass(eachPass, pwdFile, hshFile)
    #    if pwdCorrect:
    #        print('Cracked the password for user: '+userNm+', it is: '+eachPass)
    #        sys.exit(0)
    #    else:
    #        print('Not right password')

def main():
    if userNm in passDict:
        print('User '+userNm+' found on passwd file, will try to crack it')
        pass_in_file=passDict[userNm]
        salt_in_file=pass_in_file.split(';;;')[0]
        pswd_in_file=pass_in_file.split(';;;')[1]
        hackTry(pswd_in_file, salt_in_file)
    else:
        print('User '+userNm+' does not exist on passwd file, cant do nothing.')


if __name__ == "__main__":
    main()
