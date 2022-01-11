
import ray
from ray import serve
import requests

ray.init("anyscale://raj-test2")
serve.start(detached=True)

@serve.deployment
def hello2(request):
  return "A different response"

hello2.deploy()
