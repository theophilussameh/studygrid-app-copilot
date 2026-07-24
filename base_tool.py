from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class every tool must inherit from.

    Each subclass must define:
      - `name`: must match the "name" used in the tool's JSON schema
                in tools.py (this is what the LLM sends back in
                tool_call.function.name).
      - `execute(**kwargs)`: runs the tool and returns a JSON-serializable
                object (dict / list / str).
    """

    name: str

    @abstractmethod
    def execute(self, **kwargs):
        ...
        