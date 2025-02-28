import sys
sys.path.append("packages/assistant/stateful")
import history

class Mock:
    def __init__(self):
        self.messages = []
    def add(self, msg):
        self.messages.append(msg)

def test_stateful():
    mock = Mock()
    args = {}
    hi = history.History(args)
    msg = "user:hello"
    hi.save(msg)
    state = hi.id()
    hi.load(mock)
    assert mock.messages[-1]== msg

    args["state"] = state
    hi = history.History(args)
    msg = "user:hi"
    assert hi.save(msg) == state
    mock = Mock()
    hi.load(mock)
    assert len(mock.messages) == 2
    assert mock.messages[-1]== msg

