import os, requests as req
def test_api_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/assistant/api"
    
    res = req.get(url).json()
    
    assert res.get("output").startswith("Hello")

    msg = { "input": "What is the capital of italy"}
    res = req.post(url, json=msg).json()
    assert res.get("output").find("Rom") 
