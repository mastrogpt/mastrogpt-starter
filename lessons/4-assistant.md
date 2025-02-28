---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
color: 266089
html: true

---
![bg left:50% 70%](assets/nuvolaris-logo.png)

### Developing Open LLM applications with

<center>
<img width="100%"src="assets/openserverless-logo.png">
</center>

## Lesson 4

## Stateful Assistant & OpenAI API 

---
![bg left:50% 80%](assets/mastrogpt.png)

## Stateful Assistant & OpenAI API 

- OpenAI api

- A chat class

- Redis

- An stateful assistant

---


![bg](https://fakeimg.pl/700x400/ff0000,0/0A6BAC?retina=1&text=OpenAI+API)

---

# OpenAI API Intro

- The first API developed
  - the "de-facto" standard

- Everyone uses it
  - We can use it with private AI also

  - You can hook in other providers

---

# OpenAI API: create a connection

- `base_url`: the location of the api key server
- `api_key`: the authentication key (if required)

```python
import os, openai
# ollama configuratin
host =  os.getenv("OLLAMA_HOST")
api_key = os.getenv("AUTH")
base_url = f"https://{api_key}@{host}/v1"
# accessing to the server
client = openai.OpenAI(
    base_url = base_url,
    api_key = api_key,
)
```

---
# <!--fit--> OpenAI API: `messages` is a list of message

- a message: 

```json
message = {
    "role": "user",
    "content": "What is the capital of Italy"
}
```

- Roles:
  - `system`: configuration 
  - `user`: user requests
  - `assistant`: assistant responses 

---
# OpenAI API: completions

 Request: `messages` is a list of message:

```python
MODEL= "llama3.1:8b"
messages = [message]
res = client.chat.completions.create(
    model=MODEL,
    messages=[message],
)
```
Response:
```
res.choices[0].message.content
```
---

# OpenAI API: streaming

- Add `stream: True`

```python
res = client.chat.completions.create(
    model=MODEL,
    messages=[message],
    stream = True
)
```
Receive a stream:

```python
for m in res: 
   print(m.choices[0].delta.content)
```

---

![bg](https://fakeimg.pl/700x400/ff0000,0/0A6BAC?retina=1&text=Chat+Class)

---

# Classes in Python

```python
class Counter:
  def __init__(self):
    self.value = 0

  def count(self):
    self.value += 1
    return self.value
```
Esempio:
```
c = Counter()
c.count()
c.count()
```

---
# Wrapping OpenAI

- Inspecting the code
`!code packages/assistant/api/chat.py`
- Testing the Chat class
```python
import sys ; sys.path.append("packages/assistant/api") ; import chat
ch = chat.Chat({})
ch.add("system:I tell the country and you tell me the capital.")
ch.complete()
ch.add("user:Italy")
ch.complete()
ch.add("user:France")
ch.complete()
ch.messages
```

---

# Exercise: add streaming to Chat

- Search `TODO:E4.1`
  - add the `stream` function adapted to the openai API  
  - save the `args` in a field to find the socket
  - request a stream from OpenAI api
  - stream the response from OpenAI api
  - activate the streaming in the response
 
 ---

![bg](https://fakeimg.pl/700x400/ff0000,0/0A6BAC?retina=1&text=Redis)

---

# Introducing REDIS

REmote DIctionary Server
- a fast cache of data structures (string list map etc)
- the backbone of serverless applications
 
```python
import os, redis
prefix = os.getenv("REDIS_PREFIX")
redis_url = os.getenv("REDIS_URL")
rd = redis.from_url(redis_url)
```
# NOTE: you have **always** to use a prefix

---

### REDIS python examples
```python
rd.set(f"{prefix}test", "hello")
rd.get(f"{prefix}test")
```
`True`
`b'hello'`

```python
rd.rpush(f"{prefix}list", "first")
rd.rpush(f"{prefix}list", "second")
for item in rd.lrange(f"{prefix}list", 0, -1):
  print(item)
```
`b'first'`
`b'second'`


---
# <!--fit--> Many other commands and data structures

- **Hashes**
  -  Commands: `HSET`, `HGET`
- **Sets**
  -  Commands: `SADD`, `SMEMBERS`
- **Sorted Sets**
  - Commands: `ZADD`, `ZRANGE`
- Many more: **Bitmaps**,  **Streams**, **HyperLogLogs**...

---

![bg](https://fakeimg.pl/700x400/ff0000,0/0A6BAC?retina=1&text=Assistant)

---

# A History class 

- How to store the state in REDIS
   - generate an unique key for storing a state
   - expiring this key in one day
```python
import uuid
key = prefix+"assistant:"+str(uuid.uuid4())
rd.rpush(key, "test")
rd.expire(key, 86400)
```
   - store and recover this ID in the `state` field

`
!code packages/assistant/stateful/history.py
`

---
# A History Class: testing

- Testing the History class 
```python
import sys ; sys.path.append("packages/assistant/stateful")
import history, chat
# saving state   
hi = history.History({})
hi.save("system:I tell the country you tell the capital")
hi.id()
# recovering the state
hi = history.History({"state": hi.id()})
hi.save("user:Rome")
ch = chat.Chat({})
hi.load(ch)
ch.messages
```

---
# Implementation of a stateful chat

```python
# load the history in the chat
hi = history.History(args)
ch = chat.Chat(args)
hi.load(ch)
# add a message and save it 
msg = f"user:{inp}"
ch.add(msg)
hi.save(msg)
# complete, save the assistant and return the id
out = ch.complete()
hi.save(f"assistant:{out}")
res['state'] = hi.id()
```
---
# Exercise: add history to chat
- Search `TODO:E4.2`
  - Reload the history from redis
  - Initialize the chat with the history
  - Save the answer from the LLM
  - Return the id of the history as state