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

## Lesson 1 

# First Steps

---
![bg left:50% 80%](assets/mastrogpt.png)

### Agenda

- Integrated Services

- Examples: the `hello`s

- CLI tools 

- Exercise: reverse

- About Nuvolaris

- What is next?

---

![bg](https://fakeimg.pl/700x400/ff0000,0/0A6BAC?retina=1&text=Integrated+Services)


---

![bg right:50% 90%](1-setup/tests.png)

# `hello` package

- Collection samples for all the services
- Launching the tests verifies all the services
- Also useful for interacting and debugging
- Servics are all both `local`  
 and `remote`

--- 
# <!--fit--> Exercise: fixing a failing test (trivial bug)

- Search for the `TODO:` string
- Investigate why a test is failing
- Fix it and run the unit test
- Deploy and run the integration test

<center><img src="1-setup/fixbug.png"></center>

---

![bg](https://fakeimg.pl/350x200/ff0000,0/0A6BAC?retina=1&text=Examples:+the+"hello"s)

---
![bg right:50% 90%](1-setup/ollama.png)

# `hello/llm` 

- Access to the LLM
- Ollama with
  - `llama3.1:8b`
    - powerful small model          
  - `llama3.2-vision:11b`
    - with vision capabilities 
  - `mxbai-embed-large:latest`
    - embedding model 

---

![bg right:50% 90%](1-setup/stream.png)

# `hello/stream`

- An example of the streamer
- Return the ASCII of each caratecter
- Stream the input in 1 second interval

----
![bg right:50% 90%](1-setup/redis.png)

# `hello/cache`

- Talk directly with REDIS
- Useful for debugging
- Remember there is a required `PREFIX` for the keys!
  - `<username>:`

----

![bg right:50% 90%](1-setup/s3.png)

# `hello/store`

- S3 Storage
- Files are uploaded here
- Simple commands:
  - `*<prefix>` list content by prefix
  - `!<prefix>` remove content by prefix
  - `+<file>=<content>` create a file on the fly

---

![bg right:50% 90%](1-setup/milvus.png)

# `hello/vdb`

- Milvus Vector Database
- Store what you type
- Simple commands:
  - `*<search>` vector search
  - `!<word>` remove entries containing a word


---
![bg](https://fakeimg.pl/350x200/ff0000,0/0A6BAC?retina=1&text=CLI+Tools)

--- 
 
 # <!--fit-->`ops` docs on https://openserverless.apache.org

 - It is also self-documenting:

```sh
ops               # main help message
ops -h            # list embedded tools
ops -t            # list tasks 
```
We will use mostly:
- `ops ide`  support 
- `ops ai`   A.I. oriented plugin

---
# `ops` essentials
- basics commands to manage actions

```
ops action list
ops action create reverse lessons/reverse.py
ops invoke reverse
ops invoke reverse input=hello
ops url reverse
curl https://openserverless.dev/api/v1/namespaces/msciab/actions/reverse
ops action update reverse lessons/reverse.py --web true
ops url reverse
curl https://openserverless.dev/api/v1/web/msciab/default/reverse
curl "https://openserverless.dev/api/v1/web/msciab/default/reverse?input=hello"
ops action delete reverse
ops action list
```

--- 
# `ops ide` essentials

- manages packaging and hot-reload
```
ops ide                           # support tools main subcommand
ops ide login                     # login to one openserverless instance
ops ide deploy                    # package and deploy all the actions
ops ide deploy hello/llm          # package and deploy one action
ops ide devel                     # incremental development mode   
ops ide clean                     # clean temporary files
```

---

# `ops ai` essential
- our AI-oriented plugin
```
ops ai                 # help
ops ai lesson          # download lessons and solutions
ops ai user            # update users
ops ai chat            # command line chat
ops ai cli             # the Python REPL 
ops ai new             # create a new service
```
---

![bg](https://fakeimg.pl/350x200/ff0000,0/0A6BAC?retina=1&text=Exercise:+reverse)


---

# <!--fit--> Exercise: implement a `reverse` chat
- `ops ai new reverse msciab`
- implement the code to a reverse  functions
   - read input, return output
   - if empty input, return usage
- `ops ide deploy msciab/reverse`
- Add the service to `packages/mastrogpt/index/90-Tests.json`
- Use it in Pinocchio

---

![bg](https://fakeimg.pl/350x200/ff0000,0/0A6BAC?retina=1&text=About+Nuvolaris)


---

![bg](assets/architecture.png)

---

![bg 95%](1-setup/pricelist.png)

---

![bg](https://fakeimg.pl/350x200/ff0000,0/0A6BAC?retina=1&text=What+is+Next?)


---

# Lesson 2 - Streaming Chat

 Implementing an LLM chat with streaming support

## More lessons
- Lesson 3: Form Support
- Lesson 4: Building an Assistant
- Lesson 5: Vision Support
- Lesson 6: VectorDB
- Lesson 7: Bulding a RAG

