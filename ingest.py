import json


def load_faq_data(path="data/studygrid_faq.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)