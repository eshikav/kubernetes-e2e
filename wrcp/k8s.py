from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import os

class k8sHelper():
    def __init__(self,
                 token_file_path = '/var/run/secrets/kubernetes.io/serviceaccount/token',
                 api_prefix='Bearer',
                 host=None,
                 ssl_cert_path='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'):
        self.token = token_file_path
        self.api_prefix = api_prefix
        #Todo: Get value from environment varable
        self.host = "https://192.168.206.1:6443"
        self.ssl_cert_path = ssl_cert_path
        self.config = self.getConfig()

    def getConfig(self):
       configuration = kubernetes.client.Configuration()
       with open(self.token, 'r') as f:
        token = f.read()
       configuration.api_key["authorization"] = token
       configuration.api_key_prefix['authorization'] = self.api_prefix
       configuration.host = self.host
       configuration.ssl_ca_cert = self.ssl_cert_path
       return kubernetes.client.ApiClient(configuration)

class Pods():
    def __init__(self, api_client, namespace=None):
      self.api_client = api_client
      self.namespace  = namespace
      self.pods       = {}
    def getPods(self):
      api_instance = kubernetes.client.CoreV1Api(self.api_client)
      if self.namespace == None:
        api_response = api_instance.list_pod_for_all_namespaces()
      else:
        api_response=api_instance.list_namespaced_pod(self.namespace)
      for item in api_response.items:
        self.pods[item.metadata.name] = {}
        self.pods[item.metadata.name]['status'] = item.status.phase
        self.pods[item.metadata.name]['reason'] = item.status.reason
        self.pods[item.metadata.name]['message'] = item.status.message
        self.pods[item.metadata.name]['ip'] = item.status.pod_ip
      return self.pods

    def getPodsStatus(self):
      pod_list = self.getPods()
      print(pod_list)
      pod_status = [ True if pod_list[item]['status'] != "Running" else False for item in pod_list]
      return pod_status
    
class Deployments(Pods):
    def __init__(self, api_client, namespace=None):
        super().__init__(name)
    
    def getDeployments():
        pass
