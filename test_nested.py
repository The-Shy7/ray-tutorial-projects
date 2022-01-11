import requests
import escapism
import string
import subprocess
import sys
import time
import ray
from ray import serve
from starlette.requests import Request

# Pre-formatted code
HEADER_STUB = '''
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
'''

ray.init(address="auto", namespace="serve")
serve.start(detached=True)

def provision_serve_deployment(script):
    code_obj_ref = ray.put(script)
    python_code = ray.get(code_obj_ref)
    
    format_code = f'''
@serve.deployment(route_prefix="/factorial")
{python_code}
    
factorial.deploy()
'''
    
    exec(format_code)
    
    print(serve.list_deployments())
    
def main():
    provision_serve_deployment(HEADER_STUB)
    # print(requests.get("http://127.0.0.1:8000/factorial?number=4").text)
    deployment = serve.get_deployment("factorial")
    handle = deployment.get_handle()
    print(ray.get(handle.remote(3)))
    print(ray.get(handle.remote(5)))
    print(ray.get(handle.remote(4)))
    print(ray.get(handle.remote(6)))

if __name__ == "__main__":
    main()