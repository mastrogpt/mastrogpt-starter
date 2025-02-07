import sys, requests as req
sys.path.append("tests")
sys.path.append("packages/chat/stateless")
import streamock
import stateless

def test_url():
    base = stateless.url({})[:-12]
    assert req.get(base).text == 'Ollama is running'

def test_stream():
    # init mock
    args = streamock.args()
    llm = stateless.url(args) 
    mock = streamock.start(args)
    # invoke the request
    msg = { "model": "llama3.1:8b", "prompt": "What is the capital of Italy?", "stream": True} 
    lines = req.post(llm, json=msg).iter_lines()
    out = stateless.stream(args, lines)
    assert out.find("{") == -1
    assert out.find("Rom") != -1 
    stream = streamock.stop(mock).decode("utf-8")
    assert out.find("{") == -1
    assert stream.find("Rom") != -1
     
