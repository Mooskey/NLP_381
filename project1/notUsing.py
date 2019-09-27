###PRE-PROCESSING###
brown_train_source = open('brown-train.txt', 'r').read()

#parse by sentence
brown_train_sentence_parsed = brown_train_source.split(' .')

brown_train = ''

for i in range(0, len(brown_train_sentence_parsed)):
    #pad and lowercase each sentence
    brown_train_sentence_parsed[i] = ' <s> ' + brown_train_sentence_parsed[i].lower() + ' </s> .'
    #reinstitute it into corpus
    brown_train = brown_train + brown_train_sentence_parsed[i]

#corpus cleaning
brown_train = brown_train[1:]    
brown_train = brown_train.replace('\n','')

#brown train split into tokens
brown_train_token_parsed = brown_train.split(' ')


#Counts each token
total_token_count = 0
token_counts = dict()

for word in brown_train_token_parsed:
    
    total_token_count +=1

    if token_counts.get(word) == None:
        token_counts[word] = 0
        
    token_counts[word] += 1

#Assign counts of 1 to unknown token

token_counts_unk = token_counts

token_counts_unk['<unk>'] = 0

remove_list = list()

for token in token_counts_unk:
    if token_counts_unk[token] == 1:

        #replace token in corpus with unknown
        brown_train = brown_train.replace(token, '<unk>')
        #reallocate token count to unknown
        token_counts_unk['<unk>'] += 1
        remove_list.append(token)

#remove token from list
for token in remove_list:
    del token_counts_unk[token]
