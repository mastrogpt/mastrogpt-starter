import os, requests as req
def test_summarization():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/summarization"
    res = req.get(url).json()
    assert res.get("output") == "summarization"
