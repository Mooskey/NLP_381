class Document:

    def __init__(self,text = ''):
        self.doc_text = text
        self.total_token_count = 0
        self.token_counts = {}

        self.cleanDoc()
        self.countTokens()


    def cleanDoc(self, pad=True, lower=True):
        if(pad == False and lower == False):
            print('Nothing to do.')
        else: 
        #parse by sentence
            sentence_parsed_doc = self.doc_text.split(' .')

            self.doc_text = ''

            for i in range(0, len(sentence_parsed_doc)):
            #pad and lowercase each sentence
                sentence_parsed_doc[i] = ' <s> ' + sentence_parsed_doc[i].lower() + ' </s> .'
            #reinstitute it into corpus
                self.doc_text = self.doc_text + sentence_parsed_doc[i]

        #corpus cleaning
            self.doc_text = self.doc_text[1:]    
            self.doc_text = self.doc_text.replace('\n','')
            if '  ' in self.doc_text:
                self.doc_text  = self.doc_text.replace('  ', ' ')
            
    
    def countTokens(self):
        token_parsed_doc = self.doc_text.split(' ')
        for token in token_parsed_doc:
                
            self.total_token_count +=1

            if self.token_counts.get(token) == None:
                self.token_counts[token] = 0
                
            self.token_counts[token] += 1
    
    def trainUnknownify(self):
        unknowned_text = str(self.doc_text)
        tokens = self.token_counts.keys()
        for token in tokens:
            if self.token_counts[token] == 1:
                unknowned_text = unknowned_text.replace(' ' + token + ' ', ' <unk> ')
        return Document(unknowned_text)

    def testUnknownify(self, doc):
        unknowned_text = str(self.doc_text)
        test_tokens = set(self.token_counts.keys())
        train_tokens = set(doc.token_counts.keys())
        test_exclusive_tokens = test_tokens - train_tokens
        for token in test_exclusive_tokens:
            unknowned_text = unknowned_text.replace(' ' + token + ' ', ' <unk> ')
        return Document(unknowned_text)

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
        tokens = self.token_counts.keys()
        for token in tokens:
            if bigram_mle.get(token) == None:
                bigram_mle[token] = {'bigram_count' : 0}
            for token2 in tokens:
                if bigram_mle[token].get(token2) == None:
                    bigram_mle[token][token2] = 0

    #go through document
        token_parsed_doc = self.doc_text.split(' ')
        
        for i in range(1, self.total_token_count):

        #add one to the total number of bigrams that is conditioned on the previous word.
            bigram_mle[token_parsed_doc[i-1]]['bigram_count'] += 1
        #add one to the count of current word given (within the dictionary of the) previous word
            bigram_mle[token_parsed_doc[i-1]][token_parsed_doc[i]] += 1
        
    #divide each sub-dictionary by its super dictionary's bigram count
        for token in tokens:
            bigram_count = bigram_mle[token]['bigram_count']
            for token2 in tokens:
                bigram_mle[token][token2] = bigram_mle[token][token2]/bigram_count
            bigram_mle[token]['bigram_count'] = bigram_count
        
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
        token_parsed_doc = self.doc_text.split(' ')
        for i in range(1, self.total_token_count):

        #add one to the total number of bigrams that is conditioned on the previous word.
            bigram_smoothed[token_parsed_doc[i-1]]['bigram_count'] += 1
        #add one to the count of current word given (within the dictionary of the) previous word
            bigram_smoothed[token_parsed_doc[i-1]][token_parsed_doc[i]] += 1
        
    #divide each sub-dictionary by its super dictionary's bigram count
        for token in tokens:
            bigram_count = bigram_smoothed[token]['bigram_count']
            for token2 in tokens:
                bigram_smoothed[token][token2] = bigram_smoothed[token][token2]/bigram_count
            bigram_smoothed[token]['bigram_count'] = bigram_count
        
        return bigram_smoothed

    def percentTypeDiff(self, doc, model):
        if(model == 'unigram'):
            self_word_types = set(self.token_counts.keys())
            comp_word_types = set(doc.token_counts.keys())
            
            distinct_types = self_word_types - comp_word_types
            percent_distinct_types = round(100*len(distinct_types)/len(self_word_types), 2)

            return percent_distinct_types

        elif(model == 'bigram'):
            pass

    def percentTokenDiff(self, doc, model):
        if(model == 'unigram'):
            comp_word_types = set(doc.token_count.keys())
            distinct_tokens = 0
            for token in self.doc_text:
                if token not in comp_word_types:
                    distinct_tokens +=1

            percent_distinct_tokens = 100*distinct_tokens/self.total_token_count

            return percent_distinct_tokens

        elif(model == 'bigram'):
            pass