import os, requests as req
def test_world_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/hello/world"
    res = req.get(url).json()
    assert res.get("output") == "Hello, world"
    res = req.post(url, {"input": "Mike"}).json()
    assert res.get("output") == "Hello, Mike"
