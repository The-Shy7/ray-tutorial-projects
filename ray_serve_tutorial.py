import ray
from ray import serve
from fastapi import FastAPI

# write python script to serve counter class over HTTP

# start single-node ray cluster on your local machine
# allows to use all CPU cores to serve requests in parallel
ray.init()

# start ray serve runtime 
# when python script exits, ray serve shuts down
# if want to keep ray serve running in background, 
# can use serve.start(detached=True)
serve.start(detached=True)

app = FastAPI()

# define counter class
# exposes three HTTP routes
# serve class behind HTTP endpoint using ray serve
@serve.deployment # made this class into Deployment 
@serve.ingress(app)
class Counter:
  def __init__(self):
      self.count = 0

  @app.get("/")
  def get(self):
      return {"count": self.count}

  @app.get("/incr")
  def incr(self):
      self.count += 1
      return {"count": self.count}

  @app.get("/decr")
  def decr(self):
      self.count -= 1
      return {"count": self.count}
  
Counter.deploy()