import requests
import escapism
import string
import subprocess
import sys
import time
import ray
from ray import serve

# Pre-formatted code and libraries
required_libraries = '''
["ray[serve]", "requests==2.26.0"]
'''

HEADER_STUB_1 = '''
import ray
from ray import serve
import requests

ray.init(address="auto", namespace="serve")
serve.start(detached=True)

@serve.deployment
def hello1(request):
  return "Some random response"

hello1.deploy()
'''

HEADER_STUB_2 = '''
import ray
from ray import serve
import requests

ray.init("anyscale://test-serve-error", allow_public_internet_traffic=True, autosuspend=-1)
serve.start(detached=True)

@serve.deployment
def hello2(request):
  return "A different response"

hello2.deploy()
'''

ray.init("anyscale://test-serve-error", namespace="serve", allow_public_internet_traffic=True, autosuspend=-1)
serve.start(detached=True)

#######
# API #
#######
def provision_serve_deployment(script, libraries):
    """
    Provision serve deployment on existing anyscale cluster
    """
    
    # Create new python file 
    python_file = open("deploy_test.py", "w+")
    
    # Write script into previously created python file
    python_file.write(script)
    python_file.close() 
    
    # Run python file and receive deployment endpoint
    subprocess.run(["python", "deploy_test.py"])
    time.sleep(15)
    
    # Return a dictionary of active deployments (maps deployment names to deployment obj)
    print(serve.list_deployments())
         
def unprovision_serve_deployment(deployment_id):
    # Check if deployment actually exists
    # If it does exist, then delete it, otherwise, don't do anything
    if deployment_id in serve.list_deployments():
        # Make serve deployment delete request to Anyscale
        serve.get_deployment(deployment_id).delete()
    
        # Return updated dictionary of active deployments
        print(serve.list_deployments())
    else:
        pass

def main():
    provision_serve_deployment(HEADER_STUB_1, required_libraries)

if __name__ == "__main__":
    main()