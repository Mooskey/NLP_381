import re

class Document:

    def __init__(self, text = '', dirty = True):
        self.doc_text = text
        self.total_token_count = 0
        self.token_counts = {}

        if dirty == True:
            self.cleanDoc()

        self.token_parsed_doc = self.doc_text.split(' ')

        self.countTokens()


    def cleanDoc(self):
    
    #parse sentence with endings . , ? ? , and ! !
        regex_parse = '( \.\n)|( ! !\n)|( \? \?\n)'
        sentence_parsed_doc = re.split(regex_parse, self.doc_text.lower())
        
    #remove line breaks
        sentence_parsed_doc = [y.replace('\n', ' ') for y in sentence_parsed_doc if y != None]
        
    #remove trailing garbage
        del(sentence_parsed_doc[-1])
        sentence_parsed_doc[-1] = sentence_parsed_doc[-1][:-1]

    #attach padding to each of the sentences
        for i in range(0,len(sentence_parsed_doc),2):
            sentence_parsed_doc[i] = '<s> ' + sentence_parsed_doc[i] + ' </s>'
    
    #piece corpus back together
        self.doc_text = ''
        for sentence in sentence_parsed_doc:
            self.doc_text += sentence

    
    def countTokens(self):
        for token in self.token_parsed_doc:
                
            self.total_token_count +=1

            if self.token_counts.get(token) == None:
                self.token_counts[token] = 0
                
            self.token_counts[token] += 1
    
    def trainUnknownify(self):
        unknowned_text = str()
        for token in self.token_parsed_doc:
            if self.token_counts[token] == 1:
                token = '<unk>'
            unknowned_text += ' ' + token + ' '
        return Document(unknowned_text, False)

    def testUnknownify(self, doc):
        unknowned_text = str(self.doc_text)
        test_tokens = set(self.token_counts.keys())
        train_tokens = set(doc.token_counts.keys())
        test_exclusive_tokens = test_tokens - train_tokens
        for token in test_exclusive_tokens:
            unknowned_text = unknowned_text.replace(' ' + token + ' ', ' <unk> ')
        #in case the same word appears twice. I should do this with a regex but I need to brush up on those.
            unknowned_text = unknowned_text.replace(' ' + token + ' ', ' <unk> ')
        return Document(unknowned_text, False)

    def generateUnigramMLE(self):
    #create new dictionary of all words in training corpus and their counts
        unigram_mle = dict(self.token_counts)
    #divide each count by the total words in the corpus
        tokens = unigram_mle.keys()
        for token in tokens:
            unigram_mle[token] = unigram_mle[token]/self.total_token_count
        return unigram_mle
    
    def generateBigramMLE(self):
    #Create a nested dictionary of all token bigrams and a size
        bigram_mle = dict()
        tokens = set(self.token_counts.keys())
        for x in tokens:
            bigram_mle[x] = {'bigram_count' : 0}
            for y in tokens:
                bigram_mle[x][y] = 0

    #go through document
        for i in range(1, len(self.token_parsed_doc)):
            prev = self.token_parsed_doc[i-1]
            curr = self.token_parsed_doc[i]
            bigram_mle[prev][curr] += 1
            bigram_mle[prev]['bigram_count'] += 1

    #divide each sub-dictionary by its super dictionary's bigram count to get conditional probabilities
        for token in tokens:
            bigram_count = bigram_mle[token]['bigram_count']
            for token2 in tokens:
                bigram_mle[token][token2] = bigram_mle[token][token2]/bigram_count
            bigram_mle[token]['bigram_count'] = bigram_count

    #return nested dictionary of conditional probabilities    
        return bigram_mle

    def generateBigramSmoothed(self):
        bigram_smoothed = dict()
        tokens = self.token_counts.keys()
        for token in tokens:
            if bigram_smoothed.get(token) == None:
                bigram_smoothed[token] = {'bigram_count' : 0}
            for token2 in tokens:
                if bigram_smoothed[token].get(token2) == None:
                    bigram_smoothed[token][token2] = 1
                    bigram_smoothed[token]['bigram_count'] += 1
    #go through document
        for i in range(1, self.total_token_count):

        #add one to the total number of bigrams that is conditioned on the previous word.
            bigram_smoothed[self.token_parsed_doc[i-1]]['bigram_count'] += 1
        #add one to the count of current word given (within the dictionary of the) previous word
            bigram_smoothed[self.token_parsed_doc[i-1]][self.token_parsed_doc[i]] += 1
        
    #divide each sub-dictionary by its super dictionary's bigram count
        for token in tokens:
            bigram_count = bigram_smoothed[token]['bigram_count']
            for token2 in tokens:
                bigram_smoothed[token][token2] = bigram_smoothed[token][token2]/bigram_count
            bigram_smoothed[token]['bigram_count'] = bigram_count
        
        return bigram_smoothed

    def percentTypeDiff(self,  model_type, doc = None, model = None):
        if(model_type not in ['unigram', 'bigram']):
            raise ValueError('Model must be unigram or bigram')
        if(doc == None and model ==None):
            raise ValueError('Must provide a comparison set')
        if((doc == None or model!=None) and model_type == 'unigram'):
            raise ValueError('Unigram model requires document input')
        elif((model == None or doc != None) and model_type == 'bigram'):
            raise ValueError('Bigram model requires model input')

        if(model_type == 'unigram'):
            self_types = set(self.token_counts.keys())
            comp_types = set(doc.token_counts.keys())
            
            distinct_types = self_types - comp_types

        elif(model_type == 'bigram'):          
            distinct_types = set()
            self_types = set()
            for i in range(1, self.total_token_count):
                prev_word = self.token_parsed_doc[i-1]
                curr_word = self.token_parsed_doc[i]
                self_types.add(prev_word + ' ' + curr_word)

                if(model[prev_word][curr_word] == 0):
                    distinct_types.add(prev_word + ' ' + curr_word)

        print(len(distinct_types))
        percent_distinct_types = round(100*len(distinct_types)/len(self_types), 2)

        return percent_distinct_types    
                



    def percentTokenDiff(self,  model_type, doc = None, model = None):
        if(model_type not in ['unigram', 'bigram']):
            raise ValueError('Model must be unigram or bigram')
        if(doc == None and model ==None):
            raise ValueError('Must provide a comparison set')
        if((doc == None or model!=None) and model_type == 'unigram'):
            raise ValueError('Unigram model requires document input')
        elif( (model == None or doc != None) and model_type == 'bigram'):
            raise ValueError('Bigram model requires model input')

        distinct_tokens = 0

        if(model_type == 'unigram'):
        #find the tokens that only appear in the document this is called on
            word_types = set(self.token_counts.keys())
            comp_word_types = set(doc.token_counts.keys())
            diff = word_types - comp_word_types

        #sum the count of each of those tokens
            for token in diff:
                distinct_tokens += self.token_counts[token]

            percent_distinct_tokens = 100*distinct_tokens/self.total_token_count

        elif(model_type == 'bigram'):
            for i in range(1, self.total_token_count):

                prev_word = self.token_parsed_doc[i-1]
                curr_word = self.token_parsed_doc[i]

                if(model[prev_word].get(curr_word) in [0, None]):
                    distinct_tokens +=1

            percent_distinct_tokens = 100*distinct_tokens/self.total_token_count - 1
        
        return percent_distinct_tokens
    