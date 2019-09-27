class Document:
    total_token_count = 0
    token_counts = dict()

    def __init__(self,text = ''):
        self.doc_text = text
        self.cleanDoc()


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
            self.countTokens()
    
    def countTokens(self):
        token_parsed_doc = self.doc_text.split(' ')
        for token in token_parsed_doc:
                
            self.total_token_count +=1

            if self.token_counts.get(token) == None:
                self.token_counts[token] = 0
                
            self.token_counts[token] += 1
    
    def unknownify(self):
        unknowned_text = self.doc_text
        for token in self.token_counts.keys():
            if self.token_counts[token] == 1:
                unknowned_text.replace(' ' + token, '<unk>')
        return Document(unknowned_text)
