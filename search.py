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


# Example of how a second tool would be added later:
#
# class WeatherTool(BaseTool):
#     name = "get_weather"
#
#     def __init__(self, weather_client):
#         self.client = weather_client
#
#     def execute(self, city):
#         return self.client.get_forecast(city)