# run ray start --head on the machine, then connect to the running 
# local ray cluster using ray.init(address="auto", namespace="serve") 
# in serve script(s) (this is the ray namespace, not kubernetes namespace, 
# can specify any namespace), can run multiple scripts to update deployments over time
# ray start --head = start local ray cluster
# serve start = start serve on the local ray cluster

import ray
from ray import serve

# connect to the running ray cluster
ray.init("anyscale://raj-test")
serve.start(detached=True)

@serve.deployment
def diff_func(request):
  return "something different"

diff_func.deploy()
print(serve.list_deployments())