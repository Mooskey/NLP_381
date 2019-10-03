import math

def logProbability(self, sentence, model, ngram):
    logs = list()
    if ngram == 'unigram':
        sentence = sentence.split(' ')
        for token in sentence:
            #if the token is not in our model, then the token maps to <unk>
            if model.get(token) == None:
                token = '<unk>'
            #append the log of the probability of token to the list of tokens
            logs.append(math.log2(model[token]))

    if ngram == 'bigram':
        pass

    return sum(logs)

