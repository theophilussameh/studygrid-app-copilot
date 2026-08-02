import os

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlitesearch import VectorSearchIndex


class Retriever:
    """
    Vector-search-backed retriever, persisted to a SQLite file via
    sqlitesearch. The embedding model is English-only for now
    (studygrid_faq.json). Swap model_name for a multilingual one when
    switching to studygrid_faq_bilingual.json later.
    """

    def __init__(
        self,
        documents,
        instructions,
        prompt_template,
        model_name="all-MiniLM-L6-v2",
        db_path="data/faq_vectors.db",
        keyword_fields=("section",),
    ):
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = SentenceTransformer(model_name)

        # If the .db file already exists, the index was built on a
        # previous run — open it as-is, no need to re-embed anything.
        index_already_built = os.path.exists(db_path)

        # NOTE: mode="lsh" (the sqlitesearch default) hashes vectors into
        # ~65k buckets (hash_size=16, n_tables=8). With only a few dozen
        # documents, most buckets end up empty or hold a single vector,
        # so search() can silently return 0-4 results instead of the
        # requested num_results even when a relevant document exists.
        # We use IVF with a single cluster instead: every document lands
        # in that one cluster, so search always compares the query
        # against the full corpus (exact cosine similarity reranking),
        # giving consistent, correct top-k results. This is only
        # appropriate because our corpus is tiny (dozens of documents);
        # revisit if the FAQ grows into the thousands.
        self.index = VectorSearchIndex(
            keyword_fields=list(keyword_fields),
            mode="ivf",
            n_clusters=1,
            db_path=db_path,
        )

        if not index_already_built:
            texts = [doc["question"] + " " + doc["answer"] for doc in documents]
            vectors = self.model.encode(texts)
            X = np.array(vectors)
            self.index.fit(X, documents)

    def search(self, question, num_results=5, filter_dict=None):
        query_vector = self.model.encode(question)
        return self.index.search(
            query_vector,
            num_results=num_results,
            filter_dict=filter_dict,
        )

    def close(self):
        self.index.close()