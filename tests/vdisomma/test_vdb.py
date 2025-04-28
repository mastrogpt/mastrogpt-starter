import sys 
sys.path.append("packages/vdisomma/vdb")
import vdb

def test_vdb():
    res = vdb.vdb({})
    assert res["output"] == "vdb"
