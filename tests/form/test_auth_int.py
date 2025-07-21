import os, requests as req
def test_auth_int():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/form/auth"
    login = os.environ.get("OPSDEV_HOST") + "/api/my/mastrogpt/login"
    res = req.get(url).json()
    assert res.get("output") == "you are not authenticated"
    
    args = {"token": "missing:missing"}
    res = req.post(url, json=args).json()
    assert res.get("output") == "you are not authenticated"

    args = {"token": "pinocchio:missing"}
    res = req.post(url, json=args).json()
    assert res.get("output") == "you are not authenticated"
    
    # note! you need to put the PINOCCHO_PASSWOND in the .env file to pass this test
    args = {"username": "pinocchio", "password": os.getenv("PINOCCHIO_PASSWORD") } 
    res = req.post(login, json=args).json()
    args = {"token": res.get("token")}
    res = req.post(url, json=args).json()
    assert res.get("output") == "you are authenticated"
    

    
    
