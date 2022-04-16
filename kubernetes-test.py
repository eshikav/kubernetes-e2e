from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import os


if not os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/'):
    sys.exit('Unable to find the Service Account')
API_TOKEN_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/token'
CA_CERT_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
CURRENT_NAMESPACE = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
def getConfig():
   configuration = kubernetes.client.Configuration()
   with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
      TOKEN = f.read()
   configuration.api_key["authorization"] = TOKEN
   configuration.api_key_prefix['authorization'] = 'Bearer'
   configuration.host = os.getenv('KUBERNETES_HOST', default=None)
   configuration.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
   return kubernetes.client.ApiClient(configuration)

def getpodSecurityContext(containers):
   security_context = []
   for container in containers:
     for cont in container:
       security_context.append(cont.security_context)
   return security_context

def getPods(api_client, namespace=None):
  api_instance = kubernetes.client.CoreV1Api(api_client)
  api_response=api_instance.list_namespaced_pod(namespace)
  pods = [ item for item in api_response.items ]
  return pods

def checkNoPodsRunningAsRoot(api_client, namespace=None):
   api_instance = kubernetes.client.CoreV1Api(api_client)
   api_response = api_instance.list_namespaced_pod(namespace)
   containers = [item.spec.containers for item in api_response.items]
   return getpodSecurityContext(containers)

def checkAllPodsAreRunning(api_client, namespace=None):
   api_instance = kubernetes.client.CoreV1Api(api_client)
   api_response=api_instance.list_namespaced_pod(namespace)
   pod_status = [ True if item.status.phase != "Running" else False for item in api_response.items ]
   return pod_status


#assert all(checkAllPodsAreRunning(getConfig(),'wrcp-k8s-test-suite'))
print(checkNoPodsRunningAsRoot(getConfig(),'wrcp-k8s-test-suite'))
print(getPods(getConfig(),'wrcp-k8s-test-suite'))
