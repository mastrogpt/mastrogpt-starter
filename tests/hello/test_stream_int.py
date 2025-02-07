import os, requests as req
def test_stream_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/hello/stream"
    res = req.get(url).json()
    assert res.get("output").startswith("Returning")
