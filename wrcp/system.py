from collections import defaultdict
from inspect import ArgSpec
import os
import paramiko
from paramiko import client

class sshClient():
    def __init__(self,
                hostname,
                username,
                password):
        self.client = client.SSHClient()
        self.autoadd = client.AutoAddPolicy()
        self.client.set_missing_host_key_policy(self.autoadd)
        self.client.connect(hostname='<hostname>',username=username,password=password)
        self.hosts = None
        self.controllers = None
        self.storage = None
        self.workers = None
        self.is_simplex = False
        self.is_dc = False
        self.subclouds = None

    def getConnection(self):
       return self.client

    def execute_command(self,args):
       args = ['source','/etc/platform/openrc', ';'] + args
       if isinstance(args,(list)):
          command = " ".join(args)
       else:
          command = args
       (stdin,stdout,stderr) = self.client.exec_command(command)
       return stdout,stderr
    def close(self):
       self.client.close()

    def parseData(self, data):
       lines = [ i.split('|') for i in data.readlines()]
       lines = [line for line in lines if len(line) > 1]
       parsed_data = []
       for line in lines:
         parsed_data.append([ word.strip() for word in line if len(word) > 0 ])
       return parsed_data

    def getHosts(self):
       stdout, stderr = self.execute_command(['system','host-list'])
       data = self.parseData(stdout)
       header = data.pop(0)
       finalData = defaultdict(list)
       for i in data:
         finalData[i[2]].append(dict(zip(header,i)))
       self.hosts =  finalData
       self.controllers = finalData['controller']
       self.storage = finalData['storage']
       self.workers = finalData['worker']
       if len(self.controllers) > 1:
          self.is_simplex = True

    def tryLockNodes(self, nodes=None):
       response = defaultdict(list)
       if nodes:
         for node in nodes:
           print(node['hostname'])
           stdout,stderr = self.execute_command(['system','host-lock','controller-1'])
           stdout = stdout.readlines()
           stderr = stderr.readlines()
           if len(stderr) !=0:
             response['controller-1'] = dict({'status': "failed", 'msg': stderr})
           else:
             response['controller-1'] = dict({'status': "success", 'msg': stdout})
       return response

    def getSubclouds(self):
       stdout,stderr = self.execute_command(['dcmanager','subcloud','list'])
       data = self.parseData(stdout)
       header = data.pop(0)
       finalData = defaultdict(list)
       for i in data:
          finalData['subcloud'].append(dict(zip(header,i)))
       if len(finalData['subcloud']) > 0:
          self.is_dc = True
       self.subclouds = finalData['subcloud']

object = sshClient("controller-1","sysadmin","Wind2022@")
object.getConnection()
object.getHosts()
object.getSubclouds()
print(object.is_simplex)
subclouds = [ True if subcloud['availability'] == "online" else  False for subcloud in object.subclouds ]
print(any(subclouds))
print(object.tryLockNodes(object.controllers))



object.close()
