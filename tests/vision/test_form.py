import sys, pathlib, base64, os
sys.path.append("packages/vision/form")
import vision

def test_form():
    img = base64.b64encode(pathlib.Path("tests/vision/cat.jpg").read_bytes()).decode()
    vis = vision.Vision({})
    res = vis.decode(img)
    assert res.find("cat") != -1
 