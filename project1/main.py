import DocumentClass
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

percent_brown_types = brown_test.percentTypeDiff('unigram', doc = brown_train)
percent_brown_tokens = brown_test.percentTokenDiff('unigram', doc = brown_train)

percent_learner_types = learner_test.percentTypeDiff('unigram', doc = brown_train)
percent_learner_tokens = learner_test.percentTokenDiff('unigram', doc = brown_train)


print('percent of unique brown test token types: ' + percent_brown_types )
print('percent of unique brown test token: ' + percent_brown_tokens )

print('\npercent of unique learner test token types: ' + percent_learner_types )
print('percent of unique learner test token: ' + percent_learner_tokens )

#Question 4

print('\nWhat percentage of bigrams (bigram type and bigram tokens) in each of the test corpora did not occur in training (treat <unk> as a token that has been observed).')

percent_brown_types_bigram = brown_test_unknowned.percentTypeDiff('bigram', model = bigram_mle)
percent_brown_tokens_bigram = brown_test_unknowned.percentTokenDiff('bigram', model = bigram_mle)

percent_learner_types_bigram = learner_test_unknowned.percentTypeDiff('bigram', model = bigram_mle)
percent_learner_tokens_bigram = learner_test_unknowned.percentTokenDiff('bigram', model = bigram_mle)