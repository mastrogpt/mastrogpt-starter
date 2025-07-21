import sys 
sys.path.append("packages/vdisomma/webrag")
import webrag

def test_webrag():
    res = webrag.webrag({})
    assert res["output"] == "webrag"
