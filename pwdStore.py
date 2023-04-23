import sys
sys.path.append('./lib')
import bcrypt
import getpass
from smldb import simpleDB

passDB = simpleDB('passwd.txt')
passDict = passDB.read()

print('\nAuthentication Module\n')
userNm=getpass.getuser()
userNm=input('\nUser ['+userNm+']: ') or userNm

def getNewPass():
    newPass=''
    salt = bcrypt.gensalt()
    passNotDone=True
    while passNotDone:
        print(userNm+' :: Enter New Password:')
        user_curPass1=getpass.getpass()
        print('Enter Password Again:')
        user_curPass2=getpass.getpass()
        if user_curPass1 == user_curPass2:
            newPass = bcrypt.hashpw(user_curPass1.encode(), salt)
            passNotDone=False
        else:
            print('Both passwords dont match, please try again.')
    newPass=newPass.decode()
    salt=salt.decode()
    passDB.write({userNm: salt+';;;'+newPass})
    return True

if userNm in passDict:
    curPass_in_file = passDict[userNm]
    userSalt_inFile = curPass_in_file.split(';;;')[0]
    userPass_inFile = curPass_in_file.split(';;;')[1]
    print(userNm+': Exists, will update the password')
    print(userNm+' :: Enter Current Password:')
    user_curPass_raw=getpass.getpass()
    user_curPass = bcrypt.hashpw(user_curPass_raw.encode(), userSalt_inFile.encode())
    user_curPass = user_curPass.decode()
    if userPass_inFile == user_curPass:
        print('Authentication Pass, now enter new password')
        getNewPass()
    else:
        print('Authentication Failed, try later')
        sys.exit(1)
else:   
    print(userNm+': Does Not Exists, will create a new one')
    getNewPass()
