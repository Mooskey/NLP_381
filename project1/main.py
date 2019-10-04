import DocumentClass, Extrapolation
###PRE-PROCESSING###
brown_train = DocumentClass.Document(open('texts/brown-train.txt', 'r').read())
brown_test = DocumentClass.Document(open('texts/brown-test.txt', 'r').read())
learner_test = DocumentClass.Document(open('texts/learner-test.txt', 'r').read())

brown_train_unknowned = brown_train.trainUnknownify()
brown_test_unknowned = brown_test.testUnknownify(brown_train_unknowned)
learner_test_unknowned = learner_test.testUnknownify(brown_train_unknowned)


unigram_mle = brown_train_unknowned.generateUnigramMLE()
bigram_mle = brown_train_unknowned.generateBigramMLE()
bigram_smooth = brown_train_unknowned.generateBigramSmoothed()


###POST-PROCESSING###

#Question 1

print('How many word types (unique words) are there in the training corpus? Please include the padding symbols and the unknown token.')

word_types = len(brown_train_unknowned.token_counts.keys())

print(word_types)

#Question 2

print('\nHow many word tokens are there in the training corpus?')

print(brown_train_unknowned.total_token_count)

#Question 3
print('\nWhat percentage of word tokens and word types in each of the test corpora did not occur in training?')

percent_brown_types = str(brown_test.percentTypeDiff('unigram', doc = brown_train))
percent_brown_tokens = str(brown_test.percentTokenDiff('unigram', doc = brown_train))

percent_learner_types = str(learner_test.percentTypeDiff('unigram', doc = brown_train))
percent_learner_tokens = str(learner_test.percentTokenDiff('unigram', doc = brown_train))


print('percent of unique brown test token types: ' + percent_brown_types )
print('percent of unique brown test tokens: ' + percent_brown_tokens )
#TODO fix percentages
print('\npercent of unique learner test token types: ' + percent_learner_types )
print('percent of unique learner test tokens: ' + percent_learner_tokens )

#Question 4

print('\nWhat percentage of bigrams (bigram type and bigram tokens) in each of the test corpora did not occur in training (treat <unk> as a token that has been observed).')

percent_brown_types_bigram = str(brown_test_unknowned.percentTypeDiff('bigram', model = bigram_mle))
percent_brown_tokens_bigram = str(brown_test_unknowned.percentTokenDiff('bigram', model = bigram_mle))

percent_learner_types_bigram = str(learner_test_unknowned.percentTypeDiff('bigram', model = bigram_mle))
percent_learner_tokens_bigram = str(learner_test_unknowned.percentTokenDiff('bigram', model = bigram_mle))

print('percent of unique brown test bigram token types: ' + percent_brown_types_bigram )
print('percent of unique brown test bigram tokens: ' + percent_brown_tokens_bigram )

print('\npercent of unique learner test bigram token types: ' + percent_learner_types_bigram )
print('percent of unique learner test bigram tokens: ' + percent_learner_tokens_bigram )

#Question 5

print('\nCompute the log probabilities of the following sentences under the three models. Please list all of the parameters required to compute the probabilities and show the complete calculation.')

#list of sentences
sentences = [
        '<s> he was laughed off the screen </s> .'.split(' '), 
        '<s> there was no compulsion behind them </s> .'.split(' '), 
        '<s> i look forward to hearing your reply </s> .'.split(' ')
        ]

print('Unigram MLE Model')
#calculate unigram log probability
unigram_log_prob = [Extrapolation.logProbabilities(sentence, unigram_mle, 'unigram') for sentence in sentences]

#length of sentences
length_sentence = [len(sentence) for sentence in sentences]
unigram_zeroes = list()

print('\nLog probabilities of each unigram token:')
for i in range(0, 3):
    print('Sentence ' + str(i + 1))
    for j in range(0, length_sentence[i]):
        #if the log probability is 0, add the associated word to the list of log probabilities that are zero
        if unigram_log_prob[i][j] == 0:
            unigram_zeroes.append(sentences[i][j])
        print('log2(P(' + sentences[i][j] + ')) = ' + str(unigram_log_prob[i][j]))
        
    print('Log probability of sentence ' + str(i+1) + ' = ' + str(sum(unigram_log_prob[i])))
    print('\n')

print('Bigram MLE Model')

#caclulate bigram mle log probability

bigram_mle_log_prob = [Extrapolation.logProbabilities(sentence, bigram_mle, 'bigram') for sentence in sentences]


bigram_mle_zeroes = list()

for i in range(0,3):
    print('Sentence ' + str(i + 1))
    for j in range(1, length_sentence[i]):
        prev_word = sentences[i][j-1]
        curr_word = sentences[i][j]

    #if the conditional log probability is 0, add the associated bigram to the list of log probabilities that are zero
        if bigram_mle_log_prob[i][j-1] == 0:
            bigram_mle_zeroes.append(sentences[i][j-1] + ' ' + sentences[i][j])

    #print each parameter and its conditional log probability

        print('log2(P(' + curr_word + ' | ' + prev_word + ')) = ' + str(bigram_mle_log_prob[i][j-1]))


    print('Log probability of sentence ' + str(i+1) + ' = ' + str(sum(bigram_mle_log_prob[i])))
    print('\n')


print('Bigram Smooth Model')

#caclulate bigram smooth log probability

bigram_smooth_log_prob = [Extrapolation.logProbabilities(sentence, bigram_smooth, 'bigram') for sentence in sentences]


bigram_smooth_zeroes = list()

for i in range(0,3):
    print('Sentence ' + str(i + 1))
    for j in range(1, length_sentence[i]):
        prev_word = sentences[i][j-1]
        curr_word = sentences[i][j]

    #if the conditional log probability is 0, add the associated bigram to the list of log probabilities that are zero
        if bigram_smooth_log_prob[i][j-1] == 0:
            bigram_smooth_zeroes.append(sentences[i][j-1] + ' ' + sentences[i][j])

    #print each parameter and its conditional log probability

        print('log2(P(' + curr_word + ' | ' + prev_word + ')) = ' + str(bigram_smooth_log_prob[i][j-1]))


    print('Log probability of sentence ' + str(i+1) + ' = ' + str(sum(bigram_smooth_log_prob[i])))
    print('\n')
                

print('Which of the parameters have zero values under each model? Use log base 2 in your calculations. Map words not observed in the training corpus to the <unk> token.')



print('Zero Probabilities: ', end = '') 
if unigram_zeroes == []:
    print('Empty')
else:
    for word in unigram_zeroes:
        print(word, sep=', ', end='')


print('Bigram MLE Zero Probabilities: ', end = '')
if bigram_mle_zeroes == []:
    print('Empty')
else:
    for word in bigram_mle_zeroes:
        print(word, sep=', ', end='')

print('Bigram Smooth Zero Probabilities: ', end = '')
if bigram_smooth_zeroes == []:
    print('Empty')
else:
    for word in bigram_smooth_zeroes:
        print(word, sep=', ', end='')


#Question 6

print('\nCompute the perplexities of each of the sentences above under each of the models.')

print('Unigram Perplexity')
unigram_perplexity = list()

for i in range(0,3):
    l = sum(unigram_log_prob[i])/length_sentence[i]
    unigram_perplexity.append(2**l)
    print('Sentence ' + str(i+1) + ' Perplexity: ' + str(perplexity[i]))

print('Bigram MLE Perplexity')
bigram_mle_perplexity = list()

for i in range(0,3):
    l = sum(bigram_mle_log_prob[i])/length_sentence[i]
    bigram_mle_perplexity.append(2**l)
    print('Sentence ' + str(i+1) + ' Perplexity: ' + str(bigram_mle_perplexity[i]))

print('Bigram Smooth Perplexity')
bigram_smooth_perplexity = list()

for i in range(0,3):
    l = sum(bigram_smooth_log_prob[i])/length_sentence[i]
    bigram_smooth_perplexity.append(2**l)
    print('Sentence ' + str(i+1) + ' Perplexity: ' + str(bigram_smooth_perplexity[i]))
