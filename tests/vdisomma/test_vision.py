import sys 
sys.path.append("packages/vdisomma/vision")
import vision

def test_vision():
    res = vision.vision({})
    assert res["output"] == "vision"
