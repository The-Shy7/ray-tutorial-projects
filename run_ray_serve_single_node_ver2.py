# run ray start --head on the machine, then connect to the running 
# local ray cluster using ray.init(address="auto", namespace="serve") 
# in serve script(s) (this is the ray namespace, not kubernetes namespace, 
# can specify any namespace), can run multiple scripts to update deployments over time
# ray start --head = start local ray cluster
# serve start = start serve on the local ray cluster

import ray
from ray import serve

# connect to the running ray cluster
ray.init(address="auto", namespace="serve")

@serve.deployment
def my_func(request):
  return "hello"

my_func.deploy()