import os
import openai

MODEL = "llama3.1:8b"
ROLE = "system:You are an helpful assistant."

#TODO:E4.1 add the stream function
#fix it to extract line.choices[0].delta.content
#END TODO

class Chat:
    def __init__(self, args):
        
        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        api_key = args.get("AUTH", os.getenv("AUTH"))
        base_url = f"https://{api_key}@{host}/v1"
        
        self.client = openai.OpenAI(
            base_url = base_url,
            api_key = api_key,
        )
        
        self.messages = []
        self.add(ROLE)
        
        #TODO:E4.1 
        # save args in a field
        #END TODO
        
    def add(self, msg):
        [role, content] = msg.split(":", maxsplit=1)
        self.messages.append({
            "role": role,
            "content": content,
        })
    
    def complete(self):
        #TODO:E4.1 
        # add stream: True
        res = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
        )
        # END TODO
        try: 
            #TODO:E4.1 stream the result 
            out = res.choices[0].message.content
            #END TODO
            self.add(f"assistant:{out}")
        except:
            out =  "error"
        return out
    
