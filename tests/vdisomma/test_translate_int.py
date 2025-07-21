import os, requests as req
def test_translate():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/translate"
    res = req.get(url).json()
    assert res.get("output") == "translate"
