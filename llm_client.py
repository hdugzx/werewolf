import openai
import os
import httpx
from pathlib import Path

# Method 1: Using the new OpenAI client (recommended)
# This is the modern approach using the OpenAI Python SDK
class LLMClient:
    def __init__(self, model):
        self.client = openai.OpenAI(
            api_key = os.getenv("OPENAI_API_KEY"),
            base_url = os.getenv("BASE_URL"),
            http_client = httpx.Client(verify = False)
        )
        self.model = model
    def chat(self, messages, n = 1):
        """Using the OpenAI client class - recommended approach"""
        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages,
            n = n
        )
        #print(response.choices[2].message.content)
        #print(response.choices[1].message.content)
        return response.choices[0].message.content

    def read(self, file_name):
        """Read a text file and send its contents as a single user message."""
        path = Path(__file__).resolve().parent / ("prompt/" + file_name)
        text = path.read_text(encoding = "utf-8")

        return self.chat([{"role": "user", "content": text}])

# Example usage
if __name__ == "__main__":
    # Make sure to set your OPENAI_API_KEY environment variable
    # export OPENAI_API_KEY="your-api-key-here"
    
    llm = LLMClient(model = "deepseek-chat")
    messages = [{"role": "user", "content": "output nothing"}]
    response = llm.chat(messages)
    print(f"响应:{response}")

    #print(f"响应:{llm.read('one_night_rules.txt')}")
