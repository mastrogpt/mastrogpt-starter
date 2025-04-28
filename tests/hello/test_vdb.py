import sys
sys.path.append("packages/hello/vdb")
import vdb

def test_vdb():
    vdb.vdb_init({"drop_collection": vdb.COLLECTION})
    args = {}
    db = vdb.vdb_init({})
    res = vdb.vdb({})
    assert res.get("output", "").startswith("Start with '*'")
    inp = "This is a test."
    assert vdb.vdb({"input": inp}).get("output", "").startswith("OK:")
    inp = "I want to verify if it works."
    assert vdb.vdb({"input": inp}).get("output", "").startswith("OK:")
    inp = "More text to search."
    assert vdb.vdb({"input": inp}).get("output", "").startswith("OK:")
    inp = "This is another test."
    assert vdb.vdb({"input": inp}).get("output", "").startswith("OK:")
    
    inp = "*"
    assert vdb.vdb({"input": inp}).get("output") == 'Please specify a not empty search string.'
    inp = "!"
    assert vdb.vdb({"input": inp}).get("output") == 'Please specify a not empty delete substring.'
        
    inp = "*works"
    vdb.vdb({"input": inp})
    vdb.vdb({"input": inp})
    n = vdb.vdb({"input": inp}).get("output").count('works')
    assert n >= 1

    inp = "*test"
    out = vdb.vdb({"input": inp}).get("output")
    #print(out)
    n = out.count("test")
    assert n >= 2
    
    inp = "*missing"
    n = vdb.vdb({"input": inp}).get("output").count("missing")
    assert n == 0
    
    inp = "!test"
    out = vdb.vdb({"input": inp}).get("output")
    assert out.find("Deleted: 2")!=-1
      
    inp = "*works"
    vdb.vdb({"input": inp})
    vdb.vdb({"input": inp})
    n = vdb.vdb({"input": inp}).get("output").count("works")
    assert n == 1
    
    inp = "*test"
    n = vdb.vdb({"input": inp}).get("output").count("test")
    assert n == 0

