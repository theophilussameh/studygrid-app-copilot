# build_context and build_prompt


def build_context(search_results):
    lines = []
    for doc in search_results:
        lines.append(doc['section'])
        lines.append('Q: ' + doc['question'])
        lines.append('A: ' + doc['answer'])
        lines.append('Q_AR: ' + doc['question_ar'])
        lines.append('A_AR: ' + doc['answer_ar'])
        lines.append('')
    return '\n'.join(lines).strip()