import ray
from ray import serve
from starlette.requests import Request
import requests

ray.init(address="auto", namespace="serve")
serve.start(detached=True)

# @serve.deployment(route_prefix="/outer")
# def outer_func(name):
#     if isinstance(name, Request):
#         name = name.query_params["name"]
#     def inner_func1(name):
#         def inner_func2(name):
#             return f"Hello {name}"
#         return inner_func2(name)
#     return inner_func1(name)

@serve.deployment(route_prefix="/factorial")
def factorial(number):
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

factorial.deploy()
print(requests.get("http://127.0.0.1:8000/factorial?number=4").text) # should print the integer 24, but get TypeError instead of correct input