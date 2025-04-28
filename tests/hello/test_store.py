import sys 
sys.path.append("packages/hello/store")
import store
    

def test_store():
    args = {}
    s3,bucket = store.connect(args)

    key = "test/hello"
    assert store.write(s3, bucket, "error") == "please separate file from content with '='"
    filecontent = f"{key}=world"
    assert store.write(s3, bucket, filecontent) == 'test/hello size 5'

    #print(store.show(s3,bucket,""))    
    assert store.check(s3, bucket, key) == f"{key} size 5"
    assert store.check(s3, bucket, "not/found") == "not/found not found"

    out = store.show(s3, bucket, "")
    assert out.find(key) != -1
    out = store.show(s3, bucket, "hello")
    assert out.find(key) != -1

    assert store.remove(s3, bucket, "") == 'please provide a not empty prefix'

    prefix="test/"
    out = store.remove(s3, bucket, prefix)
    assert out.find(f"removed {key}") != -1

    out = store.remove(s3, bucket, prefix)
    assert out.find(f"removed {key}") == -1
    
