import sys 
sys.path.append("packages/vdisomma/store")
import store

def test_store():
    res = store.store({})
    assert res["output"] == "store"
