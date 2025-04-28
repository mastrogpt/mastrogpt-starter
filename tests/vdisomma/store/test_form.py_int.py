import os, requests as req
def test_form.py():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/store/form.py"
    res = req.get(url).json()
    assert res.get("output") == "form.py"
