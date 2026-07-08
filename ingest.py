from minsearch import Index

# loding data

def load_faq_data():
   import json
   with open("data/studygrid_faq_bilingual.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    documents = []
    documents.extend(data)
    
    return documents


# Prepare index

def build_index(documents):
     index = Index(
    text_fields=['question', 'question_ar', 'answer', 'answer_ar'],
    keyword_fields=['section']
                  )
     index.fit(documents)
     return index
 
    
