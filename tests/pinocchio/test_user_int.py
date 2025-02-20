import os, requests as req
def test_user():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/pinocchio/user"
    res = req.get(url).json()
    assert res.get("output") == "user"
