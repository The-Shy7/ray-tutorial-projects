import ray

from fastapi import FastAPI
from ray import serve

app = FastAPI()
ray.init(address="auto", namespace="summarizer")
serve.start(detached=True)

@serve.deployment(route_prefix="/hello")
@serve.ingress(app)
class MyFastAPIDeployment:
    @app.get("/")
    def root(self):
        return "Hello, world!"

MyFastAPIDeployment.deploy()