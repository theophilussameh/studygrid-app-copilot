from tools import TOOL_SCHEMAS
from search import SearchTool
import json


class GridMindAgent:

    def __init__(
        self,
        retriever,
        openai_client,
        model="openai/gpt-oss-20b"
    ):

        self.rag = retriever
        self.search_tool = SearchTool(retriever)
        self.openai_client = openai_client
        self.model = model

        tool_instances = [SearchTool(retriever)]
        self.tools = {tool.name: tool for tool in tool_instances}
 
    

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

               response = self.llm(messages, tools=TOOL_SCHEMAS)

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
        tool = self.tools.get(tool_name)
 
        if tool is None:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
 
        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid arguments JSON from the model."})
 
        try:
            result = tool.execute(**arguments)
        except Exception as exc:
            # Feed the error back to the model instead of crashing —
            # lets the model see what went wrong and try again.
            return json.dumps({"error": str(exc)})
 
        return json.dumps(result, indent=2)
 