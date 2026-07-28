# build_context: turns search results into the text block sent to the LLM

def build_context(search_results):
    lines = []
    for doc in search_results:
        lines.append(doc['section'])
        lines.append('Q: ' + doc['question'])
        lines.append('A: ' + doc['answer'])

        # Only present in the bilingual dataset — kept optional so this
        # function works with both studygrid_faq.json (English only)
        # and studygrid_faq_bilingual.json (Arabic + English).
        if doc.get('question_ar'):
            lines.append('Q_AR: ' + doc['question_ar'])
        if doc.get('answer_ar'):
            lines.append('A_AR: ' + doc['answer_ar'])

        lines.append('')
    return '\n'.join(lines).strip()
