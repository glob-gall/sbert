import sys
from sentence_transformers import SentenceTransformer, util
import time

from getTitles import getTitles

def exec():
    if __name__ != "__main__":
        return
    
    numberOfTitles = int(sys.argv[1])
    model = SentenceTransformer('all-MiniLM-L6-v2')
 
    corpus_sentences = list(set(getTitles(numberOfTitles)))


    print("Encode the corpus. This might take a while")
    corpus_embeddings = model.encode(corpus_sentences, batch_size=64, show_progress_bar=True, convert_to_tensor=True)


    print("Start clustering")
    start_time = time.time()

    #Two parameters to tune:
    #min_cluster_size: Only consider cluster that have at least 25 elements
    #threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(corpus_embeddings, min_community_size=25, threshold=0.75)

    print("Clustering done after {:.2f} sec".format(time.time() - start_time))


    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))
        for sentence_id in cluster[0:5]:
            print("\t", corpus_sentences[sentence_id])
        # print("\t", "...")
        # for sentence_id in cluster[-3:]:
        #     print("\t", corpus_sentences[sentence_id])

exec()