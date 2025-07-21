import sys 
sys.path.append("packages/vdisomma/summarization")
import summarization

def test_summarization():
    res = summarization.summarization({})
    assert res["output"] == "summarization"
