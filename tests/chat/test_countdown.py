import sys
sys.path.append("tests")
sys.path.append("packages/chat")
import streamock
import countdown

def test_countdown():
    args = streamock.args()
    mock = streamock.start(args)
    
    lines = countdown.count_to_zero(3)
    countdown.stream(args, lines)

    res = streamock.stop(mock).decode("utf-8")
    
    assert res.startswith('{"output": "3...')
    assert res.find("Go!") != -1

