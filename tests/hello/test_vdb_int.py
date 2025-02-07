import os, requests as req
def test_vdb_int():
    vdb = os.environ.get("OPSDEV_HOST") + "/api/my/hello/vdb"
    
    args = {"drop_collection": "test"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").startswith("Start with '*'")

    args = {"input": "Hello, world."}
    res = req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    args = {"input": "Hello again, world."}
    req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    args = {"input": "We are on earth."}
    req.post(vdb, json=args).json()
    res.get("output").startswith("OK:")
    
    args = {"input": "*world"}
    # retry a few tims for timing issues
    for i in range(0, 10):
        out = req.post(vdb, json=args).json().get("output")
        if out.startswith("Found"):
            print(f"Found at {i}")
            break
        
    assert out.count("world") >= 2
    
    args = {"input": "!world"}
    res = req.post(vdb, json=args).json()
    assert res.get("output").find("Deleted: 2") != -1
        