from base_tool import BaseTool
from context import build_context


class SearchTool(BaseTool):

    name = "search"

    def __init__(self, retriever):
        self.rag = retriever

    def execute(self, query):
        search_results = self.rag.search(query)
        context = build_context(search_results)
        return {"context": context}