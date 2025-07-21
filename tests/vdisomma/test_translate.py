import sys 
sys.path.append("packages/vdisomma/translate")
import translate

def test_translate():
    res = translate.translate({})
    assert res["output"] == "translate"
