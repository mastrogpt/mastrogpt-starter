import os, requests as req
def test_form():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/store/form"
    res = req.get(url).json()
    assert res.get("output") == "form"
