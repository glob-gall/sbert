import sys
from getTitles  import *

from sentence_transformers import SentenceTransformer, util, models
from torch import nn

# model = SentenceTransformer('all-MiniLM-L6-v2')

#bert
word_embedding_model = models.Transformer('bert-base-uncased', max_seq_length=256)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(), out_features=256, activation_function=nn.Tanh())

model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model])


def exec():
    if __name__ != "__main__":
        return
    
    numberOfTitles = int(sys.argv[1])
    sentences = getTitles(numberOfTitles)

    #Encode all sentences
    embeddings = model.encode(sentences)

    #Compute cosine similarity between all pairs
    cos_sim = util.cos_sim(embeddings, embeddings)

    #Add all pairs to a list with their cosine similarity score
    all_sentence_combinations = []
    for i in range(len(cos_sim)-1):
        for j in range(i+1, len(cos_sim)):
            all_sentence_combinations.append([cos_sim[i][j], i, j])

    #Sort list by the highest cosine similarity score
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

    print("Top-5 most similar pairs:")
    for score, i, j in all_sentence_combinations[0:numberOfTitles]:
        print("{:70} \n{:70} \n {:.4f} \n\n".format(sentences[i], sentences[j], cos_sim[i][j]))


exec()