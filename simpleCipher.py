import sys
sys.path.append('./lib')
from smldb import simpleDB
import getpass
import random

myDB=simpleDB('securePass.txt')

action='enc'
if len(sys.argv) < 2:
    print('\nUsage '+sys.argv[0]+' -e <encrypt> | -d <decrypt>')
    sys.exit(1)
else:
    if sys.argv[1] == '-d':
        action='dec'

userNm=getpass.getuser()
userNm=input('User ['+userNm+']: ') or userNm


def getCphrKey():
    cphrkey=0
    #We need a key between 65 to 122
    notDone=True
    while notDone:
        cphrkey=int(random.random()*100)
        if cphrkey > 64 and cphrkey < 123:
            notDone=False
    return cphrkey

if action=='enc':
    inText=input('Enter text to encode: ')
    encKey=getCphrKey()
    encText=chr(encKey)
    for tval in inText:
        eT=chr(ord(tval)+encKey)
        encText+=chr(ord(tval)+encKey)
    print('encText=',encText)
    myDB.write({userNm:encText})
elif action=='dec':
    print('Decryption Module')
    passDB=myDB.read()
    if userNm in passDB:
        encText=passDB[userNm]
    else:
        print('Encrypted text not found on file')
        sys.exit(1)
    cnt=1
    cphrkey=''
    decText=''
    for tval in encText:
        if cnt==1:
            cphrkey=ord(tval)
            cnt+=1
        else:
            decText+=chr(ord(tval)-cphrkey)
    print('decText=',decText)
