import os, requests as req
def test_vision():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/vision"
    res = req.get(url).json()
    assert res.get("output") == "vision"
