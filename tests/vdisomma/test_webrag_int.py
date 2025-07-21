import os, requests as req
def test_webrag():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/webrag"
    res = req.get(url).json()
    assert res.get("output") == "webrag"
