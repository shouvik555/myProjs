import paramiko
import sys
import getpass
import getopt

sshC = paramiko.SSHClient()
sshC.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def sshConn(hostName):
    userNm=getpass.getuser()
    userNm=input('\nUser ['+userNm+']: ') or userNm
    userPw=getpass.getpass()
    try:
       sshC.connect(hostName,username=userNm,password=userPw.rstrip('\n'))
       stdin, stdout, stderr = sshC.exec_command('ls -l')
       retVar = stdout.read()
       print(retVar)
       sshC.close()
    except Exception as e:
       print('Exception caught, failed to connect', e)

def usage():
   print('\nUsage: ',sys.argv[0],' option')
   print('')
   print('   -n  | --name     : Host Name to SSH to')
   print('')
   print('   -h  | --help     : Print this help menu')
   print('')


def main(argv):
   hnm=''
   try:
       opts, args = getopt.getopt(argv, 'hn:',['help','name='])
       if not opts:
           usage()
           sys.exit(1)
   except getopt.GetoptError as err:
       print(str(err))
       usage
       sys.exit(2)

   for opt, arg in opts:
       if opt in ('-h', '--help'):
           usage()
           sys.exit()
       elif opt in ('-n', '--name'):
           hnm=arg
           sshConn(hnm)
       else:
           usage()
           sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])
