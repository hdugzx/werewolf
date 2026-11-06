from llm_client import LLMClient
from typing import List
import time

class Supervisor:
    def __init__(self, decode_file, model):
        self.llm = LLMClient(model)
        self.inf = ''
        self.inf += self.llm.read('one_night_rules.txt')
        self.inf = self.inf + '\n' + self.llm.read(decode_file)

    def Chat(self, messages):
        Messages = [{"role": "user", "content": self.inf + messages}]
        response = self.llm.chat(Messages)
        self.inf = self.inf + "\n" + response

        return response

    def Boardcast(self, participants: List['Participant'], messages):
        """Broadcast messages to all participants and collect their responses"""
        final_message = ''
        cnt = 0
        for participant in participants:
            cnt += 1
            start_time = time.perf_counter()
            # Send messages to each partipant and get their response
            response = participant.Chat(messages)
            final_message += response
            print(f"the {int(cnt)}th participant's response is:")
            print(response)
            elapsed = time.perf_counter() - start_time
            print(f"it takes {elapsed:.3f}s for the {int(cnt)}th participant to deal with the rule and what supervisor said")
        
        self.inf = self.inf + "\n" + final_message
        
        return final_message

class Participant:
    def __init__(self, decode_file, model):
        self.llm = LLMClient(model)
        self.inf = ''
        self.inf += self.llm.read('one_night_rules.txt')
        self.inf = self.inf + '\n' + self.llm.read(decode_file)

    def Chat(self, messages):
        Messages = [{"role": "user", "content": self.inf + messages}]
        response = self.llm.chat(Messages)
        self.inf = self.inf + "\n" + response

        return response
    
if __name__ == "__main__":
    pass