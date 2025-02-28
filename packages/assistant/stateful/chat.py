import os
import openai

MODEL = "phi4:14b"

ROLE = "system:You are an helpful assistant."

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
        
    def add(self, msg):
        [role, content] = msg.split(":", maxsplit=1)
        self.messages.append({
                "role": role,
                "content": content,
        })
        return msg
    
    def complete(self):
        res = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
        )
        out = "error"
        if len(res.choices) >0:
            out = res.choices[0].message.content
            self.add(f"assistant:{out}")
        return out
