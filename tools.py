search_tool = {
    "type": "function",
    "name": "search",
    "description": "Search the StudyGrid knowledge base to answer questions about the application, its features, study groups, tasks, courses, shared files, and other StudyGrid features.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The user's question or search query."
            }
        },
        "required": ["query"],
        "additionalProperties": False
    }
}


TOOLS = [search_tool]