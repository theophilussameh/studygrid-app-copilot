from prompts import INSTRUCTIONS, USER_PROMPT_TEMPLATE

#Now the class: RAGBase
class Retriever:

    def __init__(
        self,
        index,
        openai_client,
        instructions=INSTRUCTIONS,
        prompt_template=USER_PROMPT_TEMPLATE,
        
    ):
        self.index = index
        self.openai_client = openai_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        
        

   # search
    def search(self, question, num_results=5):
        boost_dict = {"question": 3.0, "answer": 0.5}

        return self.index.search(
            question,
            num_results=num_results,
            boost_dict=boost_dict,
           
        )
   