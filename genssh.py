import paramiko

class SSH():
   def __init__(self):
      self.__sshStatus=False
      self.__ssh = paramiko.SSHClient()
