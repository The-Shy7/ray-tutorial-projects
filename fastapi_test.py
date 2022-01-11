import ray
from ray import serve
import requests
from starlette.applications import Starlette
from starlette.requests import Request
from fastapi import FastAPI

ray.init(address="auto", namespace="serve")
serve.start(detached=True)
app = FastAPI()

@serve.deployment(route_prefix="/calc")
@serve.ingress(app)
class FactorialCalculator:
    @app.get("/fact")
    def factorial(self, number):
        # Validate input
        if isinstance(number, Request):
            number = number.query_params["number"]
        if number < 0:
            raise ValueError("Sorry. 'number' must be zero or positive.")
        
        # Calculate the factorial of number
        def inner_factorial(number):
            if number <= 1:
                return 1
            return number * inner_factorial(number - 1)
        return inner_factorial(number)
    
    @app.post("/random")
    def random_func(self, words: dict):
        keys = words["c1"]
        vals = words["c2"]
        return keys + " " + vals
    

FactorialCalculator.deploy()
print(serve.list_deployments())
