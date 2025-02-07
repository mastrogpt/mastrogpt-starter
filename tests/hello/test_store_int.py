import os, requests as req
def test_store_int():

    url = os.environ.get("OPSDEV_HOST") + "/api/my/hello/store"
    out = req.get(url).json().get("output")
    assert out.startswith("\nUsage:")

    args = {"input": "+hello=world"}
    out = req.post(url, json=args).json().get("output")
    assert out == 'hello size 5'
    
    args = {"input": "*"}
    out = req.post(url, json=args).json().get("output")
    assert out.find("hello") != -1

    args = {"input": "!hello"}
    out = req.post(url, json=args).json().get("output")
    assert out.find("removed hello") != -1

    args = {"input": "*"}
    out = req.post(url, json=args).json().get("output")
    assert out.find("hello") == -1
