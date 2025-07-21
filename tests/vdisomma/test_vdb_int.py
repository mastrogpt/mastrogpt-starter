import os, requests as req
def test_vdb():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/vdb"
    res = req.get(url).json()
    assert res.get("output") == "vdb"
