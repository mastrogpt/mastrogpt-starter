import sys, os
sys.path.append("packages/hello/cache")
import cache

def test_cache():
    args = {}
    res = cache.cache(args)
    assert res.get("output") == "Please provide a redis command."
    
    args = {"input": "SET hello world"}
    res = cache.cache(args)
    assert res.get("output") == 'True'
    
    args = {"input": "GET hello"}
    res = cache.cache(args)
    assert res.get("output") == 'world'

    args = {"input": "this is an error"}
    res = cache.cache(args)
    assert res.get("output") == """unknown command 'this', with args beginning with: 'is' 'an' 'error' """

