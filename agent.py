from tools import TOOLS
from search import SearchTool
import json


class GridMindAgent:

    def __init__(
        self,
        rag_helper,
        openai_client,
        model="openai/gpt-oss-20b"
    ):

        self.rag = rag_helper
        self.search_tool = SearchTool(rag_helper)
        self.openai_client = openai_client
        self.model = model

    
    

    def chat(self, question):

         messages = [
            {
               "role": "system",
               "content": self.rag.instructions
           },
           {
            "role": "user",
            "content": question
           }
       ]

         while True:

               response = self.llm(messages, tools=TOOLS)

               message = response.choices[0].message

               if not message.tool_calls:
                  return message.content

               messages.append(message)

               for tool_call in message.tool_calls:

                   tool_output = self.execute_tool(tool_call)

                   messages.append({
                    "role": "tool",
                   "tool_call_id": tool_call.id,
                   "content": tool_output
                 })
    
   # The llm method sends the prompt to the LLM:
    def llm(self, messages, tools=None):
       
       response = self.openai_client.chat.completions.create(
        model=self.model,
        messages=messages,
        tools=tools,
        
      )
       return response    

       
    def execute_tool(self, tool_call):

         tool_name = tool_call.function.name

         arguments = json.loads(tool_call.function.arguments)

         if tool_name == "search":

            results = self.search_tool.search(**arguments)

            return json.dumps(results, indent=2)

         raise ValueError(f"Unknown tool: {tool_name}")
    