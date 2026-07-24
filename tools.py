search_tool_schema = {
    "type": "function",
    "function": {
        "name": "search",
        "description": (
            "Search the StudyGrid knowledge base to answer questions "
            "about the application, its features, study groups, tasks, "
            "courses, shared files, and other StudyGrid features."
        ),
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
}

# Add new tool schemas here as the project grows, e.g. weather_tool_schema,
# calendar_tool_schema... then register them in TOOL_SCHEMAS below.
TOOL_SCHEMAS = [search_tool_schema]