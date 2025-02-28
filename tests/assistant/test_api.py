import sys 
sys.path.append("packages/assistant/api")
import chat

def test_api():
    args = {}
    ch = chat.Chat(args)
    msg = "user:What is the capital of Italy"
    ch.add(msg)
    out = ch.complete()
    assert out.find("Rom") != -1
    
    assert len(ch.messages) == 3
    assert ch.messages[0]['role'] == 'system'
    assert ch.messages[1]['role'] == 'user'
    assert ch.messages[2]['role'] == 'assistant'
    
