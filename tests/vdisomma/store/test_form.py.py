import sys 
sys.path.append("packages/vdisomma/store/form.py")
import form.py

def test_form.py():
    res = form.py.form.py({})
    assert res["output"] == "form.py"
