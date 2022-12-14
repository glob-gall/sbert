"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from sentence_transformers import SentenceTransformer, util
import torch

from issue import getMergedTitles,getModifiedFilesByTitle


query = 'New Sorting/Export preferences'
sentences = getMergedTitles()

if query in sentences:
    sentences.remove(query)

embedder = SentenceTransformer('all-MiniLM-L6-v2')

corpus_embeddings = embedder.encode(sentences, convert_to_tensor=True)

# Query sentences:


# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = min(5, len(sentences))
# for query in queries:
query_embedding = embedder.encode(query, convert_to_tensor=True)

# We use cosine-similarity and torch.topk to find the highest 5 scores
cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(cos_scores, k=top_k)

print("\n======================================================================================================================================")
print(f"=============================================== [Query:{query}] ===============================================")
print("======================================================================================================================================")
print("\nTop 5 most similar sentences in corpus:\n")

for score, idx in zip(top_results[0], top_results[1]):
    print(f'=======================================================[ issue - {idx} ]=======================================================\n')
    print(sentences[idx], "(Score: {:.4f})".format(score))
    files = getModifiedFilesByTitle(sentences[idx])
    print("arquivos modificados:")
    for f in files:
        print(f)
    print("\n\n\n")

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """