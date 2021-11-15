import ray
from ray import serve
import time

# start ray locally and start serve on top of it
serve.start()

@serve.deployment
def my_func(request):
  return "hello"

my_func.deploy()

# serve will be shut down once the script exits, so keep it alive manually
while True:
    time.sleep(5)
    print(serve.list_deployments())