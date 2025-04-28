import sys 
sys.path.append("packages/vdisomma/store/form")
import form

def test_form():
    res = form.form({})
    assert res["output"] == "form"
