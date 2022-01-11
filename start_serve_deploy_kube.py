import ray
from ray import serve

# connect to the running ray cluster
ray.init(address="auto", namespace="serve")
# bind on 0.0.0.0 to expose the HTTP server on external IPs
serve.start(detached=True, http_options={"host": "0.0.0.0"})

@serve.deployment(route_prefix="/hello")
def hello(request):
    return "hello world"

hello.deploy()