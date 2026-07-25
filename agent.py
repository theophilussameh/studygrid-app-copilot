
from tools import TOOL_SCHEMAS
from search import SearchTool
import json


class GridMindAgent:

    def __init__(
        self,
        retriever,
        openai_client,
        model="openai/gpt-oss-20b",
        max_iterations=5
    ):

        self.rag = retriever
        self.openai_client = openai_client
        self.model = model
        self.max_iterations = max_iterations

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

        it = 1

        while it <= self.max_iterations:

            print(f"iteration #{it}...")

            response = self.llm(messages, tools=TOOL_SCHEMAS)

            message = response.choices[0].message

            if not message.tool_calls:
                return message.content

            # Only forward the fields the Chat Completions API actually
            # accepts back as input. message.model_dump() also includes
            # extra fields (e.g. "annotations") that some providers
            # (like Groq) reject with a 400 error.
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })

            for tool_call in message.tool_calls:

                print("function_call:", tool_call.function.name, tool_call.function.arguments)

                tool_output = self.execute_tool(tool_call)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                })

            it += 1

        # Ran out of iterations — force one last call without tools so
        # the model must answer with whatever it has gathered so far.
        response = self.llm(messages, tools=None)
        return response.choices[0].message.content



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
