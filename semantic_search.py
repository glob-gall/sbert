"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from getTitles import getTitles
from sentence_transformers import SentenceTransformer, util
import torch


sentences = getTitles(9999999)

embedder = SentenceTransformer('all-MiniLM-L6-v2')

corpus_embeddings = embedder.encode(sentences, convert_to_tensor=True)

# Query sentences:
query = 'New Sorting/Export preferences'


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = min(6, len(sentences))
# for query in queries:
query_embedding = embedder.encode(query, convert_to_tensor=True)

# We use cosine-similarity and torch.topk to find the highest 5 scores
cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(cos_scores, k=top_k)

print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 5 most similar sentences in corpus:")

for score, idx in zip(top_results[0], top_results[1]):
    if sentences[idx] != query:
        print(sentences[idx], "(Score: {:.4f})".format(score))

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """