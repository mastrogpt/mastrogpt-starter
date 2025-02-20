import sys 
sys.path.append("packages/pinocchio/user")
import user

def test_user():
    res = user.user({})
    assert res["output"] == "user"
