import os, requests as req
def test_stateful():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/assistant/stateful"
    res = req.get(url).json()
    assert res.get("output").startswith("Hello")
    args = {"input": "When I say the country, you tell me the capital city today."}
    res = req.post(url, json=args).json()
    assert "state" in res
    args['state'] =  res['state']
    args['input'] = "Italy"
    res = req.post(url, json=args).json()
    assert res.get("output").find("Rom") != -1
    args['state'] =  res['state']
    args['input'] = "France"
    res = req.post(url, json=args).json()
    assert res.get("output").find("Paris") != -1
    