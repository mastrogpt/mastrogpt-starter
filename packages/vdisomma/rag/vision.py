import os
import json
import requests as req

class Vision:
    def __init__(self, args):
        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        auth = args.get("AUTH", os.getenv("AUTH"))
        self.url = f"https://{auth}@{host}/api/chat"   
        self.model = "llama3.2-vision:11b"

    @staticmethod
    def streaming(lines):
        result: str = ''
        for line in lines:
            chunk = json.loads(line.decode("UTF-8"))
            content = chunk.get("message", {}).get("content", "")
            result += content
        return result    

    def decode(self, img):
        model = self.model
        url = self.url
        message = [{"role": "user",
                    "content": "what is in this image?",
                    "images": [img]}]
        msg = {"model": model, 
               "messages": message}
        lines = req.post(url, json=msg, stream=True).iter_lines()
        result = self.streaming(lines)
        return result



        
        
