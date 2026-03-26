from openai import OpenAI
from config import Config

class Provider:
    def __init__(self, config: Config):
        self.client = OpenAI(api_key=config.api_key)
        self.model = config.model

    def chat(self, messages: list, tools: list):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            temperature=0.0,
        )
        return response.choices[0].message
