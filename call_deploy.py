import requests
import ray
from ray import serve

ray.init(address="auto", namespace="serve")
serve.start(detached=True)

# print(requests.get("http://127.0.0.1:8000/calc/fact?number=4").text)

resp = requests.post("http://127.0.0.1:8000/calc/random", json={"c1": "word", 
                                                                "c2": "some"})
print(resp.text)

handle = serve.get_deployment("FactorialCalculator").get_handle()
ref1 = handle.factorial.remote(5)
ref2 = handle.random_func.remote({"c1": "r1", "c2": "r2"})
print(ref1)
print(ref2)
print(ray.get(ref1))
print(ray.get(ref2))