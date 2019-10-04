import math

def logProbabilities(sentence, model, ngram):
    logs = list()
    model_tokens = set(model.keys())
    
#map all unseen tokens to <unk>
    for i in range(0, len(sentence)):
        if sentence[i] not in model_tokens:
            sentence[i] = '<unk>'


    if ngram == 'unigram':
        for token in sentence:
            logs.append(math.log2(model[token]))

    if ngram == 'bigram':
        for i in range(1, len(sentence)):
            prev_word = sentence[i-1]
            curr_word = sentence[i]
            
            cond_prob = model[prev_word][curr_word]

            logs.append(math.log2(model[prev_word][curr_word]))

    return logs

