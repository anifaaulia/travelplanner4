from langchain.schema import HumanMessage

class AICrewMember:
    def __init__(self, name, role, task_prompt, openaigpt4):
        self.name = name
        self.role = role
        self.task_prompt = task_prompt
        self.openaigpt4 = openaigpt4

    def perform_task(self, data):
        # Format the prompt with the provided data
        formatted_prompt = self.task_prompt.format(**data)
        
        # Prepare the message in the expected format
        messages = [HumanMessage(content=formatted_prompt)]
        
        # Get the response from the GPT-4 model
        response = self.openaigpt4(messages)
        
        return response.content.strip()
