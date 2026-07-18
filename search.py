class SearchTool:

    def __init__(self, rag_helper):
        self.rag = rag_helper

    def search(self, query):

        search_results = self.rag.search(query)

        context = self.rag.build_context(search_results)

        return {
            "context": context
        }